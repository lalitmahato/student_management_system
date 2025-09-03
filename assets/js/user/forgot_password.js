
document.addEventListener('DOMContentLoaded', function () {
    const forgotForm = document.getElementById('forgotForm');
    if (forgotForm) {
        forgotForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('forgotEmail').value;

            if (validateEmail(email)) {
                showAlert(getTranslation('resetLinkSent'), 'success');

                // Redirect to reset password page after 3 seconds
                setTimeout(() => {
                    window.location.href = resetPasswordUrl;
                }, 3000);
            } else {
                showAlert(getTranslation('validEmail'), 'error');
            }
        });
    }

    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        if (window.location.pathname !== '/login.html' && window.location.pathname !== '/') {
            window.location.href = 'login.html';
        }
    }
});