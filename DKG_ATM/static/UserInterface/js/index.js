let loginMode = 'password';

function switchLoginMode(mode) {
    loginMode = mode;
    const tabs = document.querySelectorAll('.login-tab');
    tabs.forEach(tab => {
        if (tab.textContent.toLowerCase() === mode) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    const passwordField = document.getElementById('passwordField');
    const otpField = document.getElementById('otpField');
    const passwordInput = document.getElementById('password');
    const otpInput = document.getElementById('otp');

    if (passwordField && otpField) {
        if (mode === 'password') {
            passwordField.style.display = 'block';
            otpField.style.display = 'none';
            if (passwordInput) passwordInput.required = true;
            if (otpInput) otpInput.required = false;
        } else {
            passwordField.style.display = 'none';
            otpField.style.display = 'block';
            if (passwordInput) passwordInput.required = false;
            if (otpInput) otpInput.required = true;
        }
    }
}

// Handle all DOM setup when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize mode
    switchLoginMode('password');

    // Handle "Coming Soon" navigation links
    const comingSoonLinks = document.querySelectorAll('a[href="#"]');
    comingSoonLinks.forEach(link => {
        const text = link.textContent.trim().toLowerCase();
        if (text === 'personal' || text === 'business' || text === 'wealth') {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                showComingSoon(link.textContent.trim());
            });
        }
    });

    // Close modal when clicking outside
    document.addEventListener('click', function(e) {
        const modal = document.getElementById('comingSoonModal');
        if (modal && e.target === modal) {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }
    });

    // Send OTP button listener
    const sendOtpBtn = document.getElementById('sendOtpBtn');
    if (sendOtpBtn) {
        sendOtpBtn.addEventListener('click', function () {
            const username = document.getElementById('username').value;
            const errorDiv = document.getElementById('loginError');
            const successDiv = document.getElementById('loginSuccess');

            if (!username) {
                errorDiv.textContent = "Please enter your username first.";
                errorDiv.style.display = 'block';
                return;
            }

            this.disabled = true;
            this.textContent = "Sending...";
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch('/send_login_otp/', {
                method: "POST",
                credentials: 'same-origin',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ username: username })
            })
                .then(res => {
                    if (!res.ok) {
                        return res.text().then(text => {
                            let errorMsg = '';
                            try {
                                const errData = JSON.parse(text);
                                errorMsg = errData.message;
                            } catch (e) {
                                if (text.includes("OperationalError") || text.includes("no such table")) {
                                    errorMsg = "Database Error: Database tables have not been created. Please run migrations.";
                                } else if (text.includes("SMTP") || text.includes("smtplib")) {
                                    errorMsg = "Mail Error: Failed to send OTP. Please check server SMTP credentials.";
                                } else {
                                    errorMsg = 'Server error: ' + res.status + (res.statusText ? ' (' + res.statusText + ')' : '');
                                }
                            }
                            throw new Error(errorMsg || 'Failed to send OTP. Server error ' + res.status);
                        });
                    }
                    return res.json();
                })
                .then(data => {
                    if (data.success) {
                        successDiv.textContent = data.message;
                        successDiv.style.display = 'block';
                        errorDiv.style.display = 'none';
                        setTimeout(() => { successDiv.style.display = 'none'; }, 5000);

                        let count = 60;
                        const timer = setInterval(() => {
                            this.textContent = `Resend in ${count}s`;
                            count--;
                            if (count < 0) {
                                clearInterval(timer);
                                this.disabled = false;
                                this.textContent = "Send OTP";
                            }
                        }, 1000);
                    } else {
                        errorDiv.textContent = data.message || "An error occurred.";
                        errorDiv.style.display = 'block';
                        this.disabled = false;
                        this.textContent = "Send OTP";
                    }
                })
                .catch(err => {
                    errorDiv.textContent = err.message || "An error occurred while sending OTP.";
                    errorDiv.style.display = 'block';
                    this.disabled = false;
                    this.textContent = "Send OTP";
                    console.error(err);
                });
        });
    }

    // Login Form listener
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const errorDiv = document.getElementById('loginError');
            errorDiv.style.display = 'none';
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const payload = {
                username: document.getElementById('username').value,
                method: loginMode
            };

            if (loginMode === 'password') {
                payload.password = document.getElementById('password').value;
            } else {
                payload.otp = document.getElementById('otp').value;
            }

            fetch('/login/', {
                method: "POST",
                credentials: 'same-origin',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify(payload)
            })
                .then(res => {
                    if (!res.ok) {
                        return res.text().then(text => {
                            let errorMsg = '';
                            try {
                                const errData = JSON.parse(text);
                                errorMsg = errData.message;
                            } catch (e) {
                                if (text.includes("OperationalError") || text.includes("no such table")) {
                                    errorMsg = "Database Error: Database tables have not been created. Please run migrations.";
                                } else {
                                    errorMsg = 'Server error: ' + res.status + (res.statusText ? ' (' + res.statusText + ')' : '');
                                }
                            }
                            throw new Error(errorMsg || 'Login failed. Server error ' + res.status);
                        });
                    }
                    return res.json();
                })
                .then(data => {
                    if (data.success) {
                        window.location.href = '/next_page/';
                    } else {
                        errorDiv.textContent = data.message || "Login failed.";
                        errorDiv.style.display = 'block';
                    }
                })
                .catch(err => {
                    errorDiv.textContent = err.message || "An error occurred during login.";
                    errorDiv.style.display = 'block';
                    console.error(err);
                });
        });
    }
});

function showComingSoon(feature) {
    const modal = document.getElementById('comingSoonModal');
    const featureTitle = document.getElementById('featureTitle');
    if (modal && featureTitle) {
        featureTitle.textContent = feature + ' Banking';
        // ensure modal is attached to document.body to avoid transform/positioning conflicts
        if (modal.parentElement !== document.body) document.body.appendChild(modal);
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.display = 'flex';
        // small timeout to trigger CSS animation class if needed
        setTimeout(() => modal.classList.add('show'), 10);
    }
}

function closeComingSoonModal() {
    const modal = document.getElementById('comingSoonModal');
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
    }
}
