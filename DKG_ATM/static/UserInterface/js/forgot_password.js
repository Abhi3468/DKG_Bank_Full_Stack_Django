document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('forgotForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const email = document.getElementById('email').value.trim();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const btn = form.querySelector('button[type="submit"]');
        const err = document.getElementById('errorMsg');

        err.style.display = 'none';
        btn.disabled = true;
        btn.textContent = 'Sending...';

        fetch('/forgot-password/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: 'email=' + encodeURIComponent(email)
        })
        .then(function (res) {
            if (!res.ok) throw new Error('Server error: ' + res.status);
            return res.json();
        })
        .then(function (data) {
            if (data.success) {
                window.location.href = '/verify-otp/';
            } else {
                err.textContent = data.message || 'No account found with this email.';
                err.style.display = 'block';
            }
        })
        .catch(function (error) {
            err.textContent = 'Network error. Please try again.';
            err.style.display = 'block';
            console.error('Forgot password error:', error);
        })
        .finally(function () {
            btn.disabled = false;
            btn.textContent = 'Send OTP';
        });
    });
});
