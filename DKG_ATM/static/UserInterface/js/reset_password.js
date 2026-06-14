document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('resetForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const password = document.getElementById('password').value;
        const confirm = document.getElementById('confirm').value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const btn = form.querySelector('button[type="submit"]');
        const err = document.getElementById('errorMsg');

        err.style.display = 'none';

        if (password !== confirm) {
            err.textContent = 'Passwords do not match.';
            err.style.display = 'block';
            return;
        }

        btn.disabled = true;
        btn.textContent = 'Resetting...';

        fetch('/reset-password/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: 'password=' + encodeURIComponent(password)
        })
        .then(function (res) {
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
                    throw new Error(errorMsg || 'Server error: ' + res.status);
                });
            }
            return res.json();
        })
        .then(function (data) {
            if (data.success) {
                err.textContent = 'Password reset successful! Redirecting to login...';
                err.style.background = 'rgba(16, 185, 129, 0.15)';
                err.style.color = '#34d399';
                err.style.border = '1px solid rgba(16, 185, 129, 0.4)';
                err.style.display = 'block';
                setTimeout(function () { window.location.href = '/'; }, 2000);
            } else {
                err.textContent = data.message || 'Reset failed. Session may have expired.';
                err.style.display = 'block';
            }
        })
        .catch(function (error) {
            err.textContent = error.message || 'Network error. Please try again.';
            err.style.display = 'block';
            console.error('Reset password error:', error);
        })
        .finally(function () {
            btn.disabled = false;
            btn.textContent = 'Reset Password';
        });
    });
});
