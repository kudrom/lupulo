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
        var obj = JSON.parse(event.data),
            widgets_removed = [],
            widgets_added = [];

        if('added' in obj){
            for(var name in obj.added){
                widgets_added.push(obj.added[name]);
            }
        }
        if ('removed' in obj && obj.removed.length > 0){
            widgets_removed = widgets_removed.concat(obj.removed);
        }
        if('changed' in obj){
            for(var name in obj.changed){
                widgets_removed.push(name);
                widgets_added.push(obj.changed[name]);
            }
        }

        var name;
        for(var i = 0; i < widgets_removed.length; i++){
            name = widgets_removed[i];
            if(name in widgets){
                remove_widget(name);
                $('#' + name).remove();
            }
        }

        var layout,
            widget,
            anchor;
        for(var i = 0; i < widgets_added.length; i++){
            layout = widgets_added[i];
            if(layout.name in widgets){
                continue;
            }

            // Check requirements
            anchor = $(layout.anchor);
            if(anchor.length == 0){
                console.log("[!] " + layout.anchor +
                            " anchor doesn't exist in the document.");
                continue;
            }
            if(!(layout.type in widget_constructors)){
                console.log("[!] " + layout.type +
                            " type doesn't exist as a factory of widgets.");
                continue;
            }

            // Construct the widget
            try{
                widget = new widget_constructors[layout.type](layout);
                widget.tick(widget);
            }catch(err){
                console.log(err + "\nStopping creation of widget " + layout.name);
                throw err;
                continue;
            }

            // Add it to the page
            widget.layout = layout;
            add_widget(widget);
        }
    };

    // Dictionary which stores all the widgets in the page indexed by the
    // name of the tracked event
    var widgets = {};

    // Add widget to the widgets dictionary and bind it to the 
    // data_pipe EventSource
    function add_widget(widget){
        var layout = widget.layout;
        var iid = device_selector.value === "" ? "----" : device_selector.value;
        if(iid[0] !== "-" ){
            for(var i = 0; i < layout.event_names.length; i++){
                var complete_event_name = get_complete_event_name(layout.event_names[i]);
                data_pipe.addEventListener(complete_event_name, widget.async_callback);
                widget.event_sources.push(complete_event_name);
            }
        }
        widgets[layout.name] = widget;
    }

    // Remove widget from the widgets dictionary and unbind it from the 
    // data_pipe EventSource
    function remove_widget(name){
        var widget = widgets[name];

        // Reset the last received data event of the widget
        widget.jdata = null;

        // Unbind the connections
        var event_name;
        for(var i = 0; i < widget.event_sources.length; i++){
            event_name = widget.event_sources[i];
            data_pipe.removeEventListener(event_name, widget.async_callback);
        }
        widget.event_sources = [];

        delete widgets[name];
    }

    // Private object that stores the way of constructing widgets
    var widget_constructors = {};
    // Registering in the global scope a function that manages widget_constructors
    register_widget = function(type, constructor){
        if(type in widget_constructors){
            console.log("[!] " + type + " was already registered as a widget constructor.")
        }else{
            fill_widget_prototype(constructor);
            widget_constructors[type] = constructor;
        }
    };

    // Client SSE to access the information from the backend 
    var data_pipe = new EventSource("/subscribe");
    data_pipe.addEventListener("new_widgets", new_widgets);
    data_pipe.addEventListener("new_devices", new_devices);

    // When the #device changes, all widgets should be refreshed with the 
    // new device id.
    var device_selector = document.getElementById("device");
    device_selector.addEventListener("change", function(){
        var widget;
        for(var name in widgets){
            widget = widgets[name];
            widget.clear_framebuffers();
            remove_widget(name);
            add_widget(widget);
        }
    });
})();
