var textFilterHandler = function (e) {
    var self = this;
    var $container = django.jQuery("#" + e);
    var $button = $container.find("a.button");
    var $negate = $container.find("input[type=checkbox]").first();
    var $value = $container.find("[name=value]");
    var $targets = $container.find("input,select,textarea");
    var qs = $container.data("qs");
    var timer = null;
    var updateStatus = function () {
        var newAction;
        var changed = ($value.val() != $value.data("original"))
            || ($negate.is(":checked") != $negate.data("original"));
        if (changed) {
            newAction = "filter";
            console.log("DEBUG", "$value", $value, $value.val() == $value.data("original"), $value.val(), $value.data("original"));
            console.log("DEBUG", "$negate", $negate, $negate.is(":checked") == $negate.data("original"), $negate.is(":checked"), $negate.data("original"));
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
        if (timer === null) {
            setTimeout(updateStatus, 500);
        }
    });
    $targets.on("change", function (e) {
        updateStatus();
    });
    var getUrl = function () {
        var url;
        var action = $container.data("action");
        if (action === "clear") {
            url = qs;
        } else if ($value.val()) {
            url = qs + "&" + $value.data("lk") + "=" + $value.val();
            url = url + "&" + $negate.data("lk") + "=" + $negate.is(":checked");
        }
        return url;
    };
    self.click = function () {
        var url = getUrl();
        if (url) {
            location.href = url;
        }
    };
};
