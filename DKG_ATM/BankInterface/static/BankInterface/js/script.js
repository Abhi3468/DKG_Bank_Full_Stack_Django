document.addEventListener("DOMContentLoaded", function() {
    const verifyBtn = document.getElementById("verifyBtn");
    const withdrawBtn = document.getElementById("withdrawBtn");
    const depositBtn = document.getElementById("depositBtn");
    const pinChangeBtn = document.getElementById("pinChangeBtn");
    const historyBtn = document.getElementById("historyBtn");
    const loanBtn = document.getElementById("loanBtn");
    
    const atmActions = document.getElementById("atmActions");
    const pinSection = document.getElementById("pinSection");
    const loanSection = document.getElementById("loanSection");

    // Modal Confirm Buttons
    const confirmWithdraw = document.getElementById("confirmWithdraw");
    const confirmDeposit = document.getElementById("confirmDeposit");
    const confirmPinChange = document.getElementById("confirmPinChange");
    const confirmLoan = document.getElementById("confirmLoan");
    
    let pinVerified = false;
    let transactionChart = null;

    function getCSRFToken() {
        const cookie = document.cookie.split("; ").find(c => c.startsWith("csrftoken="));
        return cookie ? cookie.split("=")[1] : "";
    }

    function showPopup(message) {
        const popupMessage = document.getElementById("popupMessage");
        if (popupMessage) popupMessage.textContent = message;
        if (typeof openModal === "function") openModal("popupModal");
    }

    function updateDashboard(cardNumber) {
        fetch("/available_balance/", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
            body: JSON.stringify({ card_number: cardNumber })
        })
        .then(res => res.json())
        .then(data => {
            const balanceDisplay = document.getElementById('balanceDisplay');
            if (balanceDisplay) balanceDisplay.textContent = "$" + data.balance;
            updateChart(cardNumber);
        });
    }

    function updateChart(cardNumber) {
        fetch(`/analytics/${cardNumber}/`)
            .then(res => res.json())
            .then(data => {
                const canvas = document.getElementById('transactionChart');
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                if (transactionChart) transactionChart.destroy();
                transactionChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Withdrawals', 'Deposits'],
                        datasets: [{
                            data: [data.withdrawals, data.deposits],
                            backgroundColor: ['#ef4444', '#10b981'],
                            borderColor: 'transparent'
                        }]
                    },
                    options: {
                        plugins: {
                            legend: { position: 'bottom', labels: { color: '#64748b', font: { family: 'Inter', size: 12 } } }
                        }
                    }
                });
            });
    }

    // PIN Verification
    if (verifyBtn) {
        verifyBtn.addEventListener("click", function() {
            const cardPin = document.getElementById("card_pin").value;
            fetch("/verify_pin/", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify({ card_pin: cardPin })
            })
            .then(res => res.json())
            .then(data => {
                if (data.message === "Verified") {
                    pinVerified = true;
                    localStorage.setItem('card_number', data.card_number);
                    document.getElementById('displayCard').textContent = "**** **** **** " + data.card_number.slice(-4);
                    if (pinSection) pinSection.style.display = 'none';
                    if (atmActions) atmActions.style.display = 'block';
                    if (loanSection) loanSection.style.display = 'block';
                    updateDashboard(data.card_number);
                } else {
                    alert("Invalid PIN");
                }
            });
        });
    }

    // Open Modals
    if (withdrawBtn) withdrawBtn.onclick = () => openModal("withdrawModal");
    if (depositBtn) depositBtn.onclick = () => openModal("depositModal");
    if (pinChangeBtn) pinChangeBtn.onclick = () => openModal("pinModal");
    if (loanBtn) loanBtn.onclick = () => openModal("loanModal");

    // Perform Transactions
    if (confirmWithdraw) {
        confirmWithdraw.onclick = () => {
            const amount = document.getElementById("withdrawAmount").value;
            executeTransaction("/withdraw/", amount, "Withdrawal Successful! New Balance: $", "withdrawModal");
        };
    }

    if (confirmDeposit) {
        confirmDeposit.onclick = () => {
            const amount = document.getElementById("depositAmount").value;
            executeTransaction("/deposit/", amount, "Deposit Successful! New Balance: $", "depositModal");
        };
    }

    if (confirmPinChange) {
        confirmPinChange.onclick = () => {
            const newPin = document.getElementById("newPinInput").value;
            if (newPin.length === 4) {
                const cardNumber = localStorage.getItem("card_number");
                fetch("/pin_change/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
                    body: JSON.stringify({ card_number: cardNumber, new_pin: newPin })
                })
                .then(res => res.json())
                .then(data => {
                    closeModal("pinModal");
                    showPopup(data.message);
                });
            } else {
                alert("PIN must be 4 digits");
            }
        };
    }

    if (confirmLoan) {
        confirmLoan.onclick = () => {
            const amount = document.getElementById("loanAmountInput").value;
            const cardNumber = localStorage.getItem("card_number");
            fetch("/loan_request/", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
                body: JSON.stringify({ card_number: cardNumber, amount: amount })
            })
            .then(res => res.json())
            .then(data => {
                closeModal("loanModal");
                showPopup(data.message);
            });
        };
    }

    function executeTransaction(url, amount, messagePrefix, modalId) {
        if (!amount || isNaN(amount) || amount <= 0) {
            alert("Please enter a valid amount");
            return;
        }
        const cardNumber = localStorage.getItem("card_number");
        fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
            body: JSON.stringify({ card_number: cardNumber, amount: amount })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
            } else {
                closeModal(modalId);
                showPopup(messagePrefix + data.new_balance);
                updateDashboard(cardNumber);
            }
        });
    }

    if (historyBtn) {
        historyBtn.onclick = () => {
            const cardNumber = localStorage.getItem("card_number");
            if (cardNumber) window.location.href = `/history/${cardNumber}/`;
        };
    }
});
