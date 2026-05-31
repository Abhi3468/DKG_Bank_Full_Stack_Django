// ============================================
// DKG Bank Dashboard — Main Script
// ============================================

let currentCardNumber = null; // stored after PIN verification

// ---- Helpers ----
function getCookie(name) {
    let val = null;
    document.cookie.split(';').forEach(c => {
        c = c.trim();
        if (c.startsWith(name + '=')) val = decodeURIComponent(c.substring(name.length + 1));
    });
    return val;
}

function getCSRFToken() {
    // Try hidden input first, then cookie
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : getCookie('csrftoken') || '';
}

function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

function showPopup(message) {
    document.getElementById('popupMessage').textContent = message;
    openModal('popupModal');
}

// ---- PIN Verification (calls real API) ----
function verifyPin() {
    const pin = document.getElementById('card_pin').value;
    if (pin.length !== 4) {
        alert('Please enter a valid 4-digit PIN');
        return;
    }

    fetch('/verify_pin/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ card_pin: pin })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
        if (ok && data.message === 'Verified') {
            currentCardNumber = data.card_number;

            // Populate account details from verify response
            document.getElementById('displayCard').textContent = data.card_number.slice(-4);
            document.getElementById('detailAccountNumber').textContent = data.account_number || '—';
            document.getElementById('detailCustomerID').textContent = data.customer_id || '—';
            document.getElementById('detailIFSCCode').textContent = data.ifsc_code || '—';

            // Show ATM actions, hide PIN section
            document.getElementById('pinSection').style.display = 'none';
            document.getElementById('atmActions').style.display = 'block';

            // Load balance & analytics
            loadBalance();
            loadAnalytics();
        } else {
            showPopup(data.message || 'PIN verification failed.');
        }
    })
    .catch(() => showPopup('Network error. Please try again.'));
}

// ---- Load Balance ----
function loadBalance() {
    if (!currentCardNumber) return;

    fetch('/available_balance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ card_number: currentCardNumber })
    })
    .then(res => res.json())
    .then(data => {
        if (data.balance !== undefined) {
            document.getElementById('balanceDisplay').textContent = '$' + parseFloat(data.balance).toFixed(2);
        }
    })
    .catch(() => {});
}

// ---- Withdraw ----
function processWithdrawal(amount) {
    if (!currentCardNumber) { showPopup('Session expired. Please verify PIN again.'); return; }

    fetch('/withdraw/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ card_number: currentCardNumber, amount: amount })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
        closeModal('withdrawModal');
        if (ok && data.message) {
            showPopup('Withdrawal successful! Amount: $' + amount);
            loadBalance();
        } else {
            showPopup(data.error || 'Withdrawal failed.');
        }
    })
    .catch(() => showPopup('Network error.'));
}

// ---- Deposit ----
function processDeposit(amount) {
    if (!currentCardNumber) { showPopup('Session expired. Please verify PIN again.'); return; }

    fetch('/deposit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ card_number: currentCardNumber, amount: amount })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
        closeModal('depositModal');
        if (ok && data.message) {
            showPopup('Deposit successful! Amount: $' + amount);
            loadBalance();
        } else {
            showPopup(data.error || 'Deposit failed.');
        }
    })
    .catch(() => showPopup('Network error.'));
}

// ---- Change PIN ----
function changePIN(newPin) {
    if (!currentCardNumber) { showPopup('Session expired. Please verify PIN again.'); return; }

    fetch('/pin_change/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ card_number: currentCardNumber, new_pin: newPin })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
        closeModal('pinModal');
        if (ok && data.message) {
            showPopup('PIN changed successfully!');
        } else {
            showPopup(data.error || 'PIN change failed.');
        }
    })
    .catch(() => showPopup('Network error.'));
}

// ---- Loan Application ----
function applyLoan(amount) {
    if (!currentCardNumber) { showPopup('Session expired. Please verify PIN again.'); return; }

    fetch('/loan_request/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ card_number: currentCardNumber, amount: amount })
    })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
        closeModal('loanModal');
        if (ok && data.message) {
            showPopup('Loan application submitted for review!');
        } else {
            showPopup(data.error || 'Loan application failed.');
        }
    })
    .catch(() => showPopup('Network error.'));
}

// ---- Analytics (Spending Chart) ----
function loadAnalytics() {
    if (!currentCardNumber) return;

    fetch('/analytics/' + currentCardNumber + '/', {
        method: 'GET',
        headers: { 'X-CSRFToken': getCSRFToken() }
    })
    .then(res => res.json())
    .then(data => {
        initializeChart(data.withdrawals || 0, data.deposits || 0);
    })
    .catch(() => {
        // Fallback to placeholder data
        initializeChart(0, 0);
    });
}

// ---- Chart ----
let chartInstance = null;
function initializeChart(withdrawals, deposits) {
    const ctx = document.getElementById('transactionChart');
    if (!ctx) return;

    if (chartInstance) chartInstance.destroy();

    const total = withdrawals + deposits;
    const chartData = total > 0 ? [withdrawals, deposits] : [1, 1]; // placeholder if no data
    const chartLabels = ['Withdrawals', 'Deposits'];

    chartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartLabels,
            datasets: [{
                data: chartData,
                backgroundColor: ['#ef4444', '#10b981']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8' }
                }
            }
        }
    });
}

// ---- DOMContentLoaded: Wire up all buttons ----
document.addEventListener('DOMContentLoaded', function() {
    // Verify PIN
    const verifyBtn = document.getElementById('verifyBtn');
    if (verifyBtn) {
        verifyBtn.addEventListener('click', verifyPin);
    }
    // Also allow Enter key in PIN input
    const pinInput = document.getElementById('card_pin');
    if (pinInput) {
        pinInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') verifyPin();
        });
    }

    // Withdraw
    const withdrawBtn = document.getElementById('withdrawBtn');
    if (withdrawBtn) withdrawBtn.addEventListener('click', () => openModal('withdrawModal'));

    // Deposit
    const depositBtn = document.getElementById('depositBtn');
    if (depositBtn) depositBtn.addEventListener('click', () => openModal('depositModal'));

    // PIN Change
    const pinChangeBtn = document.getElementById('pinChangeBtn');
    if (pinChangeBtn) pinChangeBtn.addEventListener('click', () => openModal('pinModal'));

    // History — navigate to history page with card number
    const historyBtn = document.getElementById('historyBtn');
    if (historyBtn) {
        historyBtn.addEventListener('click', function() {
            if (currentCardNumber) {
                window.location.href = '/history/' + currentCardNumber + '/';
            } else {
                showPopup('Please verify your PIN first.');
            }
        });
    }

    // Loan
    const loanBtn = document.getElementById('loanBtn');
    if (loanBtn) loanBtn.addEventListener('click', () => openModal('loanModal'));

    // Confirm Withdraw
    const confirmWithdraw = document.getElementById('confirmWithdraw');
    if (confirmWithdraw) {
        confirmWithdraw.addEventListener('click', function() {
            const amount = document.getElementById('withdrawAmount').value;
            if (amount > 0) processWithdrawal(amount);
            else showPopup('Please enter a valid amount.');
        });
    }

    // Confirm Deposit
    const confirmDeposit = document.getElementById('confirmDeposit');
    if (confirmDeposit) {
        confirmDeposit.addEventListener('click', function() {
            const amount = document.getElementById('depositAmount').value;
            if (amount > 0) processDeposit(amount);
            else showPopup('Please enter a valid amount.');
        });
    }

    // Confirm PIN Change
    const confirmPinChange = document.getElementById('confirmPinChange');
    if (confirmPinChange) {
        confirmPinChange.addEventListener('click', function() {
            const newPin = document.getElementById('newPinInput').value;
            if (newPin.length === 4) changePIN(newPin);
            else showPopup('PIN must be exactly 4 digits.');
        });
    }

    // Confirm Loan
    const confirmLoan = document.getElementById('confirmLoan');
    if (confirmLoan) {
        confirmLoan.addEventListener('click', function() {
            const amount = document.getElementById('loanAmountInput').value;
            if (amount > 0) applyLoan(amount);
            else showPopup('Please enter a valid loan amount.');
        });
    }

    // Initialize chart with placeholder
    initializeChart(0, 0);
});
