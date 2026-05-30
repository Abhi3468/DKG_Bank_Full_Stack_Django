document.getElementById('otpForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const otp = document.getElementById('otp').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch('/verify_otp/', {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": csrfToken },
        body: "otp=" + encodeURIComponent(otp)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/reset_password/';
        } else {
            const err = document.getElementById('errorMsg');
            err.textContent = data.message;
            err.style.display = 'block';
        }
    });
});
