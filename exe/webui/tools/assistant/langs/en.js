if (typeof(_)=='undefined') {
    if (top) _ = top._
    else _ = function(str) {
        return str;
    }
}
var $i18n = {
    Assistant : _("Assistant"),
    Menu : _("Menu"),
    Previous : _("Previous"),
    Next : _("Next")
}