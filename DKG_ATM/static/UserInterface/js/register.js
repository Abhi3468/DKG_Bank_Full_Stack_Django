document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const errorDiv = document.getElementById('registerError');
    errorDiv.style.display = 'none';

    if (formData.get('password') !== formData.get('password_confirm')) {
        errorDiv.textContent = "Passwords do not match.";
        errorDiv.style.display = 'block';
        return;
    }

    fetch('/register/', {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById('successModal').style.display = 'flex';
            } else {
                const errors = JSON.parse(data.errors);
                errorDiv.innerHTML = Object.values(errors).map(err => err[0].message).join('<br>');
                errorDiv.style.display = 'block';
            }
        });
});
