document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(this);
            const errorDiv = document.getElementById('registerError');
            errorDiv.style.display = 'none';
            errorDiv.innerHTML = '';

            if (formData.get('password') !== formData.get('password_confirm')) {
                errorDiv.textContent = "Passwords do not match.";
                errorDiv.style.display = 'block';
                return;
            }

            // Disable submit button to prevent double-clicks
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creating Account...';

            fetch('/register/', {
                method: "POST",
                body: formData
            })
                .then(res => {
                    if (!res.ok) {
                        return res.text().then(text => {
                            let errorMsg = '';
                            try {
                                const errData = JSON.parse(text);
                                // Server now returns {success: false, message: '...'} on errors
                                errorMsg = errData.message || errData.errors || '';
                            } catch (e) {
                                if (text.includes("OperationalError") || text.includes("no such table") || text.includes("relation") || text.includes("does not exist")) {
                                    errorMsg = "Database Error: Database tables have not been created. Please run migrations on the server.";
                                } else if (text.includes("SMTP") || text.includes("smtplib")) {
                                    errorMsg = "Mail Error: Failed to send account details. Please check SMTP configuration.";
                                } else {
                                    errorMsg = 'Server error: ' + res.status;
                                }
                            }
                            throw new Error(errorMsg || 'Registration failed. Server error ' + res.status);
                        });
                    }
                    return res.json();
                })
                .then(data => {
                    if (data.success) {
                        const badge = document.getElementById('emailStatusBadge');
                        if (data.email_sent) {
                            badge.textContent = 'Email Sent Successfully';
                            badge.style.background = 'rgba(16, 185, 129, 0.15)';
                            badge.style.color = '#34d399';
                            badge.style.border = '1px solid rgba(16, 185, 129, 0.4)';
                        } else {
                            badge.textContent = 'Email Offline - Please Contact Support';
                            badge.style.background = 'rgba(239, 68, 68, 0.15)';
                            badge.style.color = '#f87171';
                            badge.style.border = '1px solid rgba(239, 68, 68, 0.4)';
                        }

                        document.getElementById('successModal').style.display = 'flex';
                    } else {
                        // Parse validation errors from Django's form.errors.as_json()
                        let errorMessages = [];
                        try {
                            const errors = JSON.parse(data.errors);
                            for (const field in errors) {
                                errors[field].forEach(err => {
                                    errorMessages.push(err.message);
                                });
                            }
                        } catch (parseErr) {
                            // Fallback if errors is a plain string or unexpected format
                            errorMessages.push(data.errors || data.message || 'Registration failed. Please try again.');
                        }
                        errorDiv.innerHTML = errorMessages.join('<br>');
                        errorDiv.style.display = 'block';
                    }
                })
                .catch(err => {
                    console.error('Registration error:', err);
                    errorDiv.textContent = err.message || 'Something went wrong. Please try again.';
                    errorDiv.style.display = 'block';
                })
                .finally(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                });
        });
    }
});
