// Returns the complete event name of a source event
function get_complete_event_name(source_event){
    var device = document.getElementById("device");
    var event_name = "id" + device.value + "-" + source_event;
    return event_name
}

(function (){
    // Callback for the new_devices data event source
    function new_devices(event){
        var list = JSON.parse(event.data);
        // If a new device is tracked, show it in the select form
        var device_selector = document.getElementById("device");
        for(var i = 0; i < list.length; i++){
            var option = document.createElement("option");
            option.text = list[i];
            device_selector.add(option);
        }
    };

    // Callback for the new_widgets data event source
    function new_widgets(event){
        var layouts = JSON.parse(event.data),
            layout,
            widget,
            anchor;
        for(var i = 0; i < layouts.length; i++){
            layout = layouts[i];

            // Check requirements
            anchor = $(layout.anchor);
            if(anchor.length == 0){
                console.log("[!] " + layout.anchor +
                            " anchor doesn't exist in the document.");
                continue;
            }
            if(!(layout.type in widget_factories)){
                console.log("[!] " + layout.type +
                            " type doesn't exist as a factory of widgets.");
                continue;
            }

            // Construct the widget
            try{
                widget = new widget_factories[layout.type](layout);
                widget.tick(widget);
            }catch(err){
                console.log(err + "\nStopping creation of widget " + layout.name);
                throw err;
                continue;
            }

            // Add it to the page
            for(var ii = 0; ii < layout.event_names.length; ii++){
                add_widget(widget, layout.event_names[ii]);
            }
        }
    };

    // Add widget to the widgets dictionary and bind it to the 
    // data_pipe EventSource
    function add_widget(widget, source_event){
        var iid = device_selector.value === "" ? "----" : device_selector.value;
        if(iid[0] !== "-" ){
            var complete_event_name = get_complete_event_name(source_event);
            data_pipe.addEventListener(complete_event_name, widget.async_callback);
        }else{
            var complete_event_name = "noid-" + source_event;
        }
        if(!(complete_event_name in widgets)){
            widgets[complete_event_name] = [];
        }
        widgets[complete_event_name].push(widget);
    }

    // Remove widget to the widgets dictionary and unbind it to the 
    // data_pipe EventSource
    function remove_widget(widget, event_name){
        var i = widgets[event_name].indexOf(widget);
        // Reset the last received data event of the widget
        widget.jdata = null;
        widgets[event_name].splice(i, 1);
        if(widgets[event_name].length === 0){
            delete widgets[event_name];
        }
        // If the widget was binded to any real event source (not the 
        // noid-* virtual event source)
        if(event_name[0] !== "n"){
            data_pipe.removeEventListener(event_name, widget.async_callback);
        }
    }

    // Private object that stores the way of constructing widgets
    var widget_factories = {};
    // Registering in the global scope a function that manages widget_factories
    register_widget = function(type, constructor){
        if(type in widget_factories){
            console.log("[!] " + type + " was already registered as a widget constructor.")
        }else{
            fill_widget_prototype(constructor);
            widget_factories[type] = constructor;
        }
    };

    // Dictionary which stores all the widgets in the page indexed by the
    // name of the tracked event
    var widgets = {};

    // Client SSE to access the information from the backend 
    var data_pipe = new EventSource("/subscribe");
    data_pipe.addEventListener("new_widgets", new_widgets);
    data_pipe.addEventListener("new_devices", new_devices);

    // When the #device changes, all widgets should be refreshed with the 
    // new device id.
    var device_selector = document.getElementById("device");
    device_selector.addEventListener("change", function(){
        for(var event_name in widgets){
            var len = widgets[event_name].length;
            for(var i = 0; i < len; i++){
                var last_index = widgets[event_name].length -1;
                var widget = widgets[event_name][last_index];
                widget.clear_framebuffers();
                remove_widget(widget, event_name);
                // Bind the widget to the new device id
                var source_event = event_name.split("-")[1];
                add_widget(widget, source_event);
            }
        }
    });
})();
