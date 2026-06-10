document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('otpForm');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const otp = document.getElementById('otp').value.trim();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const btn = form.querySelector('button[type="submit"]');
        const err = document.getElementById('errorMsg');

        err.style.display = 'none';
        btn.disabled = true;
        btn.textContent = 'Verifying...';

        fetch('/verify-otp/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: 'otp=' + encodeURIComponent(otp)
        })
        .then(function (res) {
            if (!res.ok) throw new Error('Server error: ' + res.status);
            return res.json();
        })
        .then(function (data) {
            if (data.success) {
                window.location.href = '/reset-password/';
            } else {
                err.textContent = data.message || 'Invalid OTP. Please try again.';
                err.style.display = 'block';
            }
        })
        .catch(function (error) {
            err.textContent = 'Network error. Please try again.';
            err.style.display = 'block';
            console.error('OTP verify error:', error);
        })
        .finally(function () {
            btn.disabled = false;
            btn.textContent = 'Verify Code';
        });
    });
});
