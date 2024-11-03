/* Funcionalidad para expandir y truncar la descripcion y los articulos */
$(document).ready(function () {
    /* Descripcion articulos */
    $('.show-more').on('click', function (e) {
        e.preventDefault();
        $(this).prev('.truncate-text').css('max-height', 'none');
        $(this).hide();
        $(this).next('.show-less').show();
    });

    $('.show-less').on('click', function (e) {
        e.preventDefault();
        $(this).prevAll('.truncate-text').css('max-height', '4.8em');
        $(this).hide();
        $(this).prev('.show-more').show();
    });

    /* Todos los articulos */
    $('.article-card:gt(2)').hide();

    $('#show-all').on('click', function (e) {
        e.preventDefault();
        $('.article-card').show();
        $(this).hide();
        $('#hide-articles').show();
    });

    $('#hide-articles').on('click', function (e) {
        e.preventDefault();
        $('.article-card').hide();
        $('.article-card:lt(3)').show();
        $(this).hide();
        $('#show-all').show();
    });
});

    