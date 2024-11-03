(function () {
    'use strict'

    var forms = document.querySelectorAll('.needs-validation')

    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }

                form.classList.add('was-validated')
            }, false)
        })
})()

/* Icono para mostrar contraseña1 */
document.addEventListener('DOMContentLoaded', function () {
    var passwordInput = document.getElementById("floatingInputGroupPassword1");
    var togglePassword = document.getElementById("togglePassword1");
    var togglePasswordIcon = document.getElementById("togglePasswordIcon1");

    togglePassword.addEventListener('click', function () {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePasswordIcon.classList.remove("fa-eye");
            togglePasswordIcon.classList.add("fa-eye-slash");
        } else {
            passwordInput.type = "password";
            togglePasswordIcon.classList.remove("fa-eye-slash");
            togglePasswordIcon.classList.add("fa-eye");
        }
    });
});

/* Icono para mostrar contraseña1 */
document.addEventListener('DOMContentLoaded', function () {
    var passwordInput = document.getElementById("floatingInputGroupPassword2");
    var togglePassword = document.getElementById("togglePassword2");
    var togglePasswordIcon = document.getElementById("togglePasswordIcon2");

    togglePassword.addEventListener('click', function () {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePasswordIcon.classList.remove("fa-eye");
            togglePasswordIcon.classList.add("fa-eye-slash");
        } else {
            passwordInput.type = "password";
            togglePasswordIcon.classList.remove("fa-eye-slash");
            togglePasswordIcon.classList.add("fa-eye");
        }
    });
});