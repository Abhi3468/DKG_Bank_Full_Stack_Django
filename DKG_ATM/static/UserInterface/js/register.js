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
