document.getElementById('resetForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const password = document.getElementById('password').value;
    const confirm = document.getElementById('confirm').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (password !== confirm) {
        const err = document.getElementById('errorMsg');
        err.textContent = "Passwords do not match.";
        err.style.display = 'block';
        return;
    }

    fetch('/reset_password/', {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded", "X-CSRFToken": csrfToken },
        body: "password=" + encodeURIComponent(password)
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Password reset successful! Please login.");
                window.location.href = '/';
            } else {
                const err = document.getElementById('errorMsg');
                err.textContent = data.message;
                err.style.display = 'block';
            }
        });
});
