var DjangoLookupFilterHandler = function (element, options) {
    var self = this;
    var config = Object.assign({negated: false, canNegate: true, button: true}, options);
    var $wrapper = django.jQuery(element);
    var $container = $wrapper.find(".filter-content ul.adminfilter");

    var $negate = $container.find("input[type=checkbox]").first();
    var $key = $container.find("input[name=key]").first();
    var $value = $container.find("input[name=value]");
    var $button = $container.find("a.button");

    var $targets = $container.find("input");
    var qs = $container.data("qs");
    var timer = null;
    var getUrl = function () {
        var url = qs;
        if ($key.val()) {
            url = qs + "&" + $key.data("lk") + "=" + $key.val();
            url = url + "&" + $value.data("lk") + "=" + $value.val();
            if (config.canNegate) {
                url = url + "&" + $negate.data("lk") + "=" + $negate.is(":checked");
            }
        }
        return url;
    };
    var updateStatus = function () {
        var newAction;
        var changed = ($key.val() != $key.data("original"))
            || ($value.val() != $value.data("original"));
        if (config.canNegate) {
            changed |= $negate.is(":checked") != $negate.data("original");
        }
        if (changed) {
            newAction = "filter";
            console.log("DEBUG", "$negate", $negate, $negate.is(":checked") == $negate.data("original"), $negate.is(":checked"), $negate.data("original"));
            console.log("DEBUG", "$key", $key, $key.val() == $key.data("original"), $key.val(), $key.data("original"));
            console.log("DEBUG", "$value", $value, $value.val() == $value.data("original"), $value.val(), $value.data("original"));
        } else {
            newAction = "clear";
        }
        console.log("DEBUG", "newAction", newAction, getUrl());
        $button.html(newAction);
        $container.data("action", newAction);
        $container.attr("data-action", newAction);
        $button.removeClass("filter").removeClass("clear").addClass(newAction);
        timer = null;
    };
    $targets.on("keyup", function (e) {
        if (e.which === 13) {
                    self.click();
        } else if (timer === null) {
            setTimeout(updateStatus, 500);
        }
    });
    self.click = function () {
        var url = getUrl();
        if (url) {
            location.href = url;
        }
    };
    $button.on("click", self.click);

};
