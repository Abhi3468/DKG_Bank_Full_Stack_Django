document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('pinForm');
    const passwordField = document.getElementById('password');
    const togglePassword = document.getElementById('togglePassword');
    const validationMessage = document.getElementById('validationMessage');

    // Initially hide the password
    passwordField.setAttribute('type', 'password');

    // Toggle password visibility
    togglePassword.addEventListener('click', function () {
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
        togglePassword.classList.toggle('bi-eye');
        togglePassword.classList.toggle('bi-eye-slash');
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        const cardNumber = document.getElementById('cardNumber').value;
        const pin = passwordField.value;

        fetch('/validate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Get CSRF token
            },
            body: JSON.stringify({ card_number: cardNumber, pin: pin })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            if (data.valid) {
                // Validation successful, redirect to next page
                window.location.href = '/next_page/';
            } else {
                // Validation failed, display error message
                if (!data.cardNumber && !data.pin) {
                    validationMessage.innerText = 'USER NOT EXISTS';
                } else {
                    validationMessage.innerText = 'USER CREDENTIALS ARE INCORRECT';
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            validationMessage.innerText = 'An error occurred. Please try again.';
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
