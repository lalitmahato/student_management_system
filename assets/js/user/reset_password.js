//
// document.addEventListener('DOMContentLoaded', function () {
//     const resetForm = document.getElementById('resetForm');
//     if (resetForm) {
//         resetForm.addEventListener('submit', function (e) {
//             e.preventDefault();
//
//             const newPassword = document.getElementById('id_new_password1').value;
//             const confirmPassword = document.getElementById('id_new_password1').value;
//
//             if (newPassword.length < 6) {
//                 showAlert(getTranslation('passwordLength'), 'error');
//                 return;
//             }
//
//             const pattern = /^(?=.*[A-Z])(?=.*\d).+$/;
//             if (!pattern.test(newPassword)) {
//                 showAlert(getTranslation('passwordRequirements'), 'error');
//                 return;
//             }
//
//             if (newPassword !== confirmPassword) {
//                 showAlert(getTranslation('passwordMismatch'), 'error');
//                 return;
//             }
//
//             showAlert(getTranslation('passwordSuccess'), 'success');
//
//             setTimeout(() => {
//                 window.location.href = loginUrl;
//             }, 3000);
//         });
//     }
//
//
//     const inputs = document.querySelectorAll('input');
//     inputs.forEach(input => {
//         input.addEventListener('focus', function () {
//             this.parentElement.classList.add('focused');
//         });
//
//         input.addEventListener('blur', function () {
//             this.parentElement.classList.remove('focused');
//         });
//     });
// });