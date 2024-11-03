// Navbar
$(document).ready(function () {
    // Cerrar menú cuando se hace clic en un enlace del menú
    $('.navbar-nav a').on('click', function () {
        $('.navbar-collapse').collapse('hide');
    });
});

