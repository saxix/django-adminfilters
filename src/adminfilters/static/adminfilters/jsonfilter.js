var jsonFieldFilterHandler = function (e) {
    var self = this;
    var $container = django.jQuery("#" + e);
    var $button = $container.find("a.button");
    var $negate = $container.find("input[type=checkbox]").first();
    var $key = $container.find("input[name=key]").first();
    var $value = $container.find("input[name=value]");
    var $options = $container.find("select[name=options]");
    var $type = $container.find("select[name=type]");
    var $targets = $container.find("input,select");
    var qs = $container.data("qs");
    var timer = null;
    var updateStatus = function () {
        var newAction;
        var changed = ($key.val() != $key.data("original"))
            || ($value.val() != $value.data("original"))
            || ($options.val() != $options.data("original"))
            || ($type.val() != $type.data("original"))
            || ($negate.is(":checked") != $negate.data("original"));
        if (changed) {
            newAction = "filter";
            console.log("DEBUG", "$negate", $negate, $negate.is(":checked") == $negate.data("original"), $negate.is(":checked"), $negate.data("original"));
            console.log("DEBUG", "$options", $options, $options.val() == $options.data("original"), $options.val(), $options.data("original"));
            console.log("DEBUG", "$key", $key, $key.val() == $key.data("original"), $key.val(), $key.data("original"));
            console.log("DEBUG", "$type", $type, $type.val() == $type.data("original"), $type.val(), $type.data("original"));
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
        } else if ($key.val()) {
            url = qs + "&" + $key.data("lk") + "=" + $key.val();
            url = url + "&" + $value.data("lk") + "=" + $value.val();
            url = url + "&" + $options.data("lk") + "=" + $options.val();
            url = url + "&" + $type.data("lk") + "=" + $type.val();
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
