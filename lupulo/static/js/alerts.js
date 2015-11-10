// Add an alert to the webpage
function add_alert(type, text){
    if(!(type in ['success', 'info', 'warning', 'danger'])){
        text = "<strong>type</strong> parameter of <strong>add_alert</strong>" +
               " is invalid.";
        type = "danger";
    }
    var button = '<button type="button" class="close" data-dismiss="alert" ' +
                 'aria-label="Close">' +
                     '<span aria-hidden="true">&times;</span>' +
                 '</button>';
    var alert_html = '<div class="alert alert-dismissible alert-' + type + '">'
                         + button + text +
                     '</div>';

    $('.warnings').append(alert_html);
}

