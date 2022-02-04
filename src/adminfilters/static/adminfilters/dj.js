var DjangoLookupFilterHandler = function (e, options) {
    var self = this;
    var config = Object.assign({negated: false, can_negate: true}, options);
    var $container = django.jQuery("#" + e);
    var $button = $container.find("a.button");
    var $negate = $container.find("input[type=checkbox]").first();
    var $key = $container.find("input[name=key]").first();
    var $value = $container.find("input[name=value]");
    var $targets = $container.find("input");
    var qs = $container.data("qs");
    var timer = null;
    var updateStatus = function () {
        var newAction;
        var changed = ($key.val() != $key.data("original"))
            || ($value.val() != $value.data("original"));
        if (config.can_negate) {
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
    var getUrl = function () {
        var url;
        var action = $container.data("action");
        if (action === "clear") {
            url = qs;
        } else if ($key.val()) {
            url = qs + "&" + $key.data("lk") + "=" + $key.val();
            url = url + "&" + $value.data("lk") + "=" + $value.val();
            if (config.can_negate) {
                url = url + "&" + $negate.data("lk") + "=" + $negate.is(":checked");
            }
        }
        return url;
    };
    $targets.on("keyup", function (e) {
        if (timer === null) {
            setTimeout(updateStatus, 500);
        }
    });
    $targets.on("change", function (e) {
        updateStatus();
    });
    self.click = function () {
        var url = getUrl();
        if (url) {
            location.href = url;
        }
    };
};
