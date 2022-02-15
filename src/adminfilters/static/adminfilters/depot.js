var DepotManager = function (element) {
    var $ = django.jQuery;
    var $wrapper = django.jQuery(element);
    var $container = $wrapper.find("ul.adminfilter");
    var $select = $container.find("select");
    var $input = $container.find("input[type=text]");
    var $buttonDelete = $container.find("a.button.delete");
    var $buttonAdd = $container.find("a.button.save");
    var qs = $container.data("qs");

    var addFilter = function () {
        if (qs !== "?") {
            var name = prompt("Filter name");
            if (name) {
                var url = qs + "&" + $container.data("lk") + "=" + encodeURIComponent(name);
                location.href = url;
            }
        }
    };
    var deleteFilter = function () {
        if (confirm(gettext("Continuing will delete selected filter configuration"))) {
            var url = "?" + $container.data("lk") + "=" + encodeURIComponent($container.data("id"));
            url += "&" + $container.data("lk-op") + "=delete";
            django.jQuery.get(url);
            location.href = qs;
        }
    };
    $select.on("change", function (e) {
        var $option = $("#depot_manager option:selected");
        var qs = $option.data("qs");
        if (qs) {
            location.href = qs;
        }
    });
    $buttonAdd.on("click", addFilter);
    $buttonDelete.on("click", deleteFilter);
    $input.on("keypress", function (e) {
        if (e.which === 13) {
            saveAs();
        }
    });

};
