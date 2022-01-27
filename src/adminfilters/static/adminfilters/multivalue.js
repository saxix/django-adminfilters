var multivalueFilter = function (e) {
    var url;
    var $button = $(e.target);
    var action = $button.data("action");
    var $area = $($button.data("textarea"));
    var $negate = $($button.data("negate"));
    var qs = $area.data("qs");
    var negated = $negate.prop("checked");
    var sel = $area.val();
    if (action === "clear") {
        url = qs;
    } else if (sel) {
        var lk = $area.data("lk");
        url = qs + "&" + lk + "=" + sel;
        if (negated) {
            url = url + "-";
        } else {
            url = url + "+";
        }
    }
    if (url) {
        location.href = url;
    }
};
