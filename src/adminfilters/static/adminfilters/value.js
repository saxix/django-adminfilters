var ValueFilterHandler = function (element, options) {
    var self = this;
    var config = Object.assign({negated: false, canNegate: true, button: true}, options);
    var $wrapper = django.jQuery(element);
    var $container = $wrapper.find(".filter-content ul.adminfilter");
    var $button = $container.find("a.button");
    var $negate = $container.find("input[type=checkbox]").first();
    var $value = $container.find("[type=text],textarea");
    var $targets = $container.find("input[type=text],textarea");
    var qs = $container.data("qs");
    var timer = null;
    var getUrl = function () {
        var url = qs;
        if ($value.val()) {
            var value = $container.data("lk") + "=" + $value.val();
            if (config.canNegate) {
                value += "&" + $container.data("lk-negated") + "=" + $negate.is(":checked");
            }
            url += "&" + value;
        }
        return url;
    };
    var updateStatus = function () {
        var newAction;
        var changed = ($value.val() != $value.data("original"));
        if (config.canNegate) {
            changed |= ($negate.is(":checked") != $negate.data("original"));
        }
        console.log("DEBUG", "$value", "changed=", $value.val() != $value.data("original"), "current=", $value.val(), "original=", $value.data("original"));
        console.log("DEBUG", "$negate", "changed=", $negate.is(":checked") != $negate.data("original"), "current=", $negate.is(":checked"), "original=", $negate.data("original"));
        if (changed) {
            newAction = "filter";
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
    $negate.on("change", function (e) {
        if (timer === null) {
            setTimeout(updateStatus, 500);
        }
    });
    $targets.on("keyup", function (e) {
        if (e.which === 13) {
            self.click();
        } else if (timer === null) {
            setTimeout(updateStatus, 500);
        }
    });
    self.click = function () {
        var url = getUrl();
        console.log(window.location.pathname + url);
        if (url) {
            location.href = url;
        }
    };
    $button.on("click", self.click);
};
