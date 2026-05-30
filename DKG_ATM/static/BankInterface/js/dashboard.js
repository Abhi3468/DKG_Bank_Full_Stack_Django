function closeModal(id) {
    document.getElementById(id).style.display = 'none';
}

function openModal(id) {
    document.getElementById(id).style.display = 'flex';
}

// PIN Verification
document.addEventListener('DOMContentLoaded', function() {
    const verifyBtn = document.getElementById('verifyBtn');
    if (verifyBtn) {
        verifyBtn.addEventListener('click', function() {
            const pin = document.getElementById('card_pin').value;
            if (pin.length === 4) {
                // PIN verification logic would go here
                document.getElementById('pinSection').style.display = 'none';
                document.getElementById('atmActions').style.display = 'block';
                loadAccountDetails();
            } else {
                alert('Please enter a valid 4-digit PIN');
            }
        });
    }

    // Withdraw Button
    const withdrawBtn = document.getElementById('withdrawBtn');
    if (withdrawBtn) {
        withdrawBtn.addEventListener('click', function() {
            openModal('withdrawModal');
        });
    }

    // Deposit Button
    const depositBtn = document.getElementById('depositBtn');
    if (depositBtn) {
        depositBtn.addEventListener('click', function() {
            openModal('depositModal');
        });
    }

    // PIN Change Button
    const pinChangeBtn = document.getElementById('pinChangeBtn');
    if (pinChangeBtn) {
        pinChangeBtn.addEventListener('click', function() {
            openModal('pinModal');
        });
    }

    // History Button
    const historyBtn = document.getElementById('historyBtn');
    if (historyBtn) {
        historyBtn.addEventListener('click', function() {
            window.location.href = '/history/';
        });
    }

    // Loan Button
    const loanBtn = document.getElementById('loanBtn');
    if (loanBtn) {
        loanBtn.addEventListener('click', function() {
            openModal('loanModal');
        });
    }

    // Confirm Withdraw
    const confirmWithdraw = document.getElementById('confirmWithdraw');
    if (confirmWithdraw) {
        confirmWithdraw.addEventListener('click', function() {
            const amount = document.getElementById('withdrawAmount').value;
            if (amount > 0) {
                processWithdrawal(amount);
            }
        });
    }

    // Confirm Deposit
    const confirmDeposit = document.getElementById('confirmDeposit');
    if (confirmDeposit) {
        confirmDeposit.addEventListener('click', function() {
            const amount = document.getElementById('depositAmount').value;
            if (amount > 0) {
                processDeposit(amount);
            }
        });
    }

    // Confirm PIN Change
    const confirmPinChange = document.getElementById('confirmPinChange');
    if (confirmPinChange) {
        confirmPinChange.addEventListener('click', function() {
            const newPin = document.getElementById('newPinInput').value;
            if (newPin.length === 4) {
                changePIN(newPin);
            }
        });
    }

    // Confirm Loan
    const confirmLoan = document.getElementById('confirmLoan');
    if (confirmLoan) {
        confirmLoan.addEventListener('click', function() {
            const amount = document.getElementById('loanAmountInput').value;
            if (amount > 0) {
                applyLoan(amount);
            }
        });
    }
});

function loadAccountDetails() {
    // Load account details from API
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    
    fetch('/api/account/details/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            document.getElementById('balanceDisplay').textContent = '$' + data.balance;
            document.getElementById('detailAccountNumber').textContent = data.account_number;
            document.getElementById('detailCustomerID').textContent = data.customer_id;
            document.getElementById('detailIFSCCode').textContent = data.ifsc_code;
            document.getElementById('displayCard').textContent = data.card_number;
        }
    });
}

function processWithdrawal(amount) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    
    fetch('/api/transaction/withdraw/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeModal('withdrawModal');
            showPopup('Withdrawal successful! Amount: $' + amount);
            loadAccountDetails();
        } else {
            showPopup('Withdrawal failed: ' + data.message);
        }
    });
}

function processDeposit(amount) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    
    fetch('/api/transaction/deposit/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeModal('depositModal');
            showPopup('Deposit successful! Amount: $' + amount);
            loadAccountDetails();
        } else {
            showPopup('Deposit failed: ' + data.message);
        }
    });
}

function changePIN(newPin) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    
    fetch('/api/account/change-pin/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ new_pin: newPin })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeModal('pinModal');
            showPopup('PIN changed successfully!');
        } else {
            showPopup('PIN change failed: ' + data.message);
        }
    });
}

function applyLoan(amount) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    
    fetch('/api/loan/apply/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeModal('loanModal');
            showPopup('Loan application submitted! Status: ' + data.status);
        } else {
            showPopup('Loan application failed: ' + data.message);
        }
    });
}

function showPopup(message) {
    document.getElementById('popupMessage').textContent = message;
    openModal('popupModal');
}

// Transaction Chart
function initializeChart() {
    const ctx = document.getElementById('transactionChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Withdrawals', 'Deposits', 'Transfers'],
                datasets: [{
                    data: [30, 50, 20],
                    backgroundColor: ['#ef4444', '#10b981', '#3b82f6']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', initializeChart);
