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
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Populate credentials in success modal
                        document.getElementById('modalCardNumber').textContent = data.card_number;
                        document.getElementById('modalCardPin').textContent = data.card_pin;
                        document.getElementById('modalAccountNumber').textContent = data.account_number;
                        document.getElementById('modalCustomerID').textContent = data.customer_id;

                        const badge = document.getElementById('emailStatusBadge');
                        if (data.email_sent) {
                            badge.textContent = 'Email Sent Successfully';
                            badge.style.background = 'rgba(16, 185, 129, 0.15)';
                            badge.style.color = '#34d399';
                            badge.style.border = '1px solid rgba(16, 185, 129, 0.4)';
                        } else {
                            badge.textContent = 'Email Offline - Write Details Down';
                            badge.style.background = 'rgba(245, 158, 11, 0.15)';
                            badge.style.color = '#fbbf24';
                            badge.style.border = '1px solid rgba(245, 158, 11, 0.4)';
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
                    errorDiv.textContent = 'Something went wrong. Please try again.';
                    errorDiv.style.display = 'block';
                })
                .finally(() => {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                });
        });
    }
});
