document.getElementById('forgotForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    fetch(document.querySelector('form').action || '/forgot_password/', {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value },
        body: "email=" + encodeURIComponent(email)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/verify_otp/';
        } else {
            const err = document.getElementById('errorMsg');
            err.textContent = data.message;
            err.style.display = 'block';
        }
    });
});
