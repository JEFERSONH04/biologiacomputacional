/* Icono para mostrar contraseña */
document.addEventListener('DOMContentLoaded', function () {
    var passwordInput = document.getElementById("OldPassword");
    var togglePassword = document.getElementById("toggleOldPassword");
    var togglePasswordIcon = document.getElementById("toggleOldPasswordIcon");

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

/* Icono para mostrar contraseña campo contraseña nueva */
document.addEventListener('DOMContentLoaded', function () {
    var passwordInput = document.getElementById("floatingInputNewPassword");
    var togglePassword = document.getElementById("toggleNewPassword");
    var togglePasswordIcon = document.getElementById("toggleNewPasswordIcon");

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

/* Icono para mostrar contraseña campo repetir contraseña */
document.addEventListener('DOMContentLoaded', function () {
    var passwordInput = document.getElementById("floatingInputNewPassword1");
    var togglePassword = document.getElementById("toggleNewPassword1");
    var togglePasswordIcon = document.getElementById("toggleNewPasswordIcon1");

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