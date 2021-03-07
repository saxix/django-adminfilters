;(function ($) {
    $('.filter-autocomplete').change(function (e) {
        var sel = $(e.target).find(':selected').val();
        var qs = $(e.target).data('ajax--qs');
        var param = $(e.target).data('ajax--param');
        location.href = `${qs}&${param}=${sel}`;
    });
})(django.jQuery);
