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

/* Icono para mostrar contraseña */
var password = document.getElementById("validationCustomPassword");
var togglePassword = document.getElementById("togglePassword");
var togglePasswordIcon = document.getElementById("togglePasswordIcon");

togglePassword.addEventListener('click', function () {
    if (password.type === "password") {
        password.type = "text";
        togglePasswordIcon.classList.remove("fa-eye");
        togglePasswordIcon.classList.add("fa-eye-slash");
    } else {
        password.type = "password";
        togglePasswordIcon.classList.remove("fa-eye-slash");
        togglePasswordIcon.classList.add("fa-eye");
    }
});