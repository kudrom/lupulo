function get_complete_event_name(source_event){
    /*
     * Returns the complete event name of a source event
     */
    var device = document.getElementById("device");
    var id = device.stable_value;
    var event_name = "id" + id + "-" + source_event;
    return event_name
};

function get_event_name(source_event){
    /*
     * Returns the event_name of the source_event.
     * This is the inverse of get_complete_event_name.
     */
    var splitted = source_event.split("-").splice(1);
    var ret = ""
    for(var i = 0; i < splitted.length; i++){
        if(i > 0){
            ret += "-";
        }
        ret += splitted[i];
    }
    return ret;
};

function pretty(obj, spaces_n, print_indexes){
    /*
     * Recursive function that returns a string which is a pretty
     * representation of the JSON object passed as an argument in obj.
     *
     * spaces_n is used to know how much tabs should be printed in each line
     * print_indexes is a flag that is used to print the indexes of a list
     * or not respectively
     */

    // Calculate the number of spaces
    var spaces = "";
    for(var i = 0; i < spaces_n ; i++){
        spaces += " ";
    }

    // Inspect the object
    var msg = "";
    if(obj instanceof Array){
        // Print a message like [a, b, c] if the object is a list or
        // [0: a, 1: b, 2: c] if print_indexes is activated
        msg += '[';
        for(var i = 0; i < obj.length; i++){
            if(print_indexes){
                if(i > 0)
                    msg += ' '
                msg += '<strong>' + i + '</strong>:';
            }
            if(obj[i] instanceof Object){
                msg += pretty(obj[i], spaces_n + 4, print_indexes);
            }else{
                if(i > 0 || print_indexes){
                    msg += " ";
                }
                msg += obj[i];
                if(i < obj.length - 1){
                    msg += ","
                }
            }
        }
        msg += ']';
    }else if(obj instanceof Object){
        // Print a message like { a: 1, b: 2} if the object is a JSON
        // object.
        var n_keys = 1;
        msg += "{\n";
        for(var key in obj){
            msg += spaces + "    " + '<strong>' + key + '</strong>: ';
            if(obj[key] instanceof Array){
                msg += pretty(obj[key], spaces_n, print_indexes);
            }else if(obj[key] instanceof Object){
                msg += pretty(obj[key], spaces_n + 4, print_indexes);
            }else{
                msg += obj[key];
            }

            if(n_keys === Object.keys(obj).length){
                msg += '\n';
            }else{
                msg += ',\n';
            }
            n_keys += 1;
        }
        msg += spaces + "}";
    }else{
        msg += obj;
    }

    return msg;
};

function validate_requirements(requirements, layout){
    /*
     * Check the requirements of a widget against a layout
     */
    var broken = false;
    for(var i = 0; i < requirements.length; i++){
        if(!(requirements[i] in layout)){
            var req = "<strong>" + requirements[i] + "</strong>";
            var name = "<strong>" + layout.name + "</strong>";
            add_alert("warning", req + " not in layout " + name);
            broken = true;
        }
    }
    if(broken){
        throw "Broken preconditions for " + layout.name;
    }
}

function add_alert(type, text){
    /*
     * Add an alert to the webpage
     */
    var types = ['success', 'info', 'warning', 'danger'];
    if(types.indexOf(type) == -1){
        text = "<strong>type</strong> parameter (<strong>" + type + "</strong>)" +
               " of <strong>add_alert</strong> is invalid.";
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

    if(type === 'danger'){
        console.error(new Error().stack);
    }
}

