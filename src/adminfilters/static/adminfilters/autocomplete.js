;(function ($) {
    $(document).ready(function () {
        $('.filter-autocomplete').on("change", function (e) {
            var sel = $(e.target).find(':selected').val();
            var qs = $(e.target).data('ajax--qs');
            if (sel) {
                var param = $(e.target).data('ajax--param');
                qs = qs + '&' + param + '=' + sel;
            }
            location.href = qs;
        });
    });
})(django.jQuery);
