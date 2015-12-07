function DefaultController(){
    // Callback for the new_devices data event source
    function new_devices(event){
        var list = JSON.parse(event.data);
        // If a new device is tracked, show it in the select form
        var device_selector = document.getElementById("device");
        var options = [];

        for(var i = 0; i < device_selector.options.length; i++){
            options.push(device_selector.options[i]);
        }

        for(var i = 0; i < list.length; i++){
            if(!(list[i] in options)){
                var option = document.createElement("option");
                option.text = list[i];
                device_selector.add(option);
            }
        }
    };

    // Callback for the new_widgets data event source
    function new_widgets(event){
        var obj = JSON.parse(event.data),
            widgets_removed = [],
            widgets_added = [];

        if('added' in obj){
            for(var name in obj.added){
                if(!(name in this.widgets))
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
            if(name in this.widgets){
                this.remove_widget(name);
                $('#' + name).remove();
            }
        }

        var layout,
            widget,
            anchor;
        for(var i = 0; i < widgets_added.length; i++){
            layout = widgets_added[i];
            if(layout.name in this.widgets){
                continue;
            }

            // Check requirements
            anchor = $(layout.anchor);
            if(anchor.length == 0){
                var text = "<strong>" + layout.anchor + "</strong>" +
                           " anchor doesn't exist in the document."
                add_alert('danger', text);
                continue;
            }
            if(!(layout.type in this.widget_constructors)){
                var text = "<strong>" + layout.type + "</strong>" +
                           " type doesn't exist as a factory of widgets.";
                add_alert('danger', text);
                continue;
            }

            // Construct the widget
            try{
                widget = new this.widget_constructors[layout.type](layout);
                widget.tick(widget);
            }catch(err){
                var name = "<strong>" + layout.name + "</strong>";
                add_alert('warning', err + ", stopping creation of widget " + name);
                console.error(err.stack);
                continue;
            }

            // Add it to the page
            widget.layout = layout;
            this.add_widget(widget);
        }
    };

    // Dictionary which stores all the widgets in the page indexed by the
    // name of the tracked event
    this.widgets = {};

    // Add widget to the widgets dictionary and bind it to the 
    // data_pipe EventSource
    this.add_widget = function(widget){
        var layout = widget.layout;

        device_selector = document.getElementById("device");
        var iid = device_selector.stable_value;
        if(iid === "")
            iid = "----";

        if(iid !== "----" ){
            for(var i = 0; i < layout.event_names.length; i++){
                var complete_event_name = get_complete_event_name(layout.event_names[i]);
                this.data_pipe.addEventListener(complete_event_name, widget.async_callback);
                widget.event_sources.push(complete_event_name);
            }
        }
        this.widgets[layout.name] = widget;
    };

    // Remove widget from the widgets dictionary and unbind it from the 
    // data_pipe EventSource
    this.remove_widget = function(name){
        var widget = this.widgets[name];

        // Reset the last received data event of the widget
        widget.jdata = null;

        // Unbind the connections
        var event_name;
        for(var i = 0; i < widget.event_sources.length; i++){
            event_name = widget.event_sources[i];
            this.data_pipe.removeEventListener(event_name, widget.async_callback);
        }
        widget.event_sources = [];

        delete this.widgets[name];
    };

    // Private object that stores the way of constructing widgets
    this.widget_constructors = {};
    // Registering in the global scope a function that manages widget_constructors
    this.register_widget = function(type, constructor){
        if(type in this.widget_constructors){
            var text = "<strong>" + type + "</strong>" +
                       " was already registered as a widget constructor.";
            add_alert("warning", text);
        }else{
            fill_widget_prototype(constructor);
            this.widget_constructors[type] = constructor;
        }
    };

    this.setup = function(){
        /*
         * Dunction called by the client to allow the injection of the this
         * object to the new_* callbacks
         */

        // Creates a wrapper around the callbacks to allow the injection of the
        // this object
        var that = this;
        function callback_wrapper(cb){
            return function(event){
                cb.call(that, event)
            };
        };
        this.new_widgets = callback_wrapper(new_widgets);
        this.new_devices = callback_wrapper(new_devices);

        // Client SSE to access the information from the backend 
        this.data_pipe = new EventSource("/subscribe");

        // stable_value is used to avoid differences in behaviour in several
        // browsers when device_selector changes its value
        device_selector = document.getElementById("device");
        device_selector.stable_value = device_selector.value;
    };

    this.connect_callbacks = function(){
        var that = this;
        this.data_pipe.addEventListener("new_widgets", this.new_widgets);
        this.data_pipe.addEventListener("new_devices", this.new_devices);
        this.data_pipe.addEventListener("new_event_sources", this.new_event_sources);

        device_selector = document.getElementById("device");
        device_selector.addEventListener("change", function (event){
            var widget;
            event.target.stable_value = event.target.value;
            for(var name in that.widgets){
                widget = that.widgets[name];
                widget.clear_framebuffers();
                that.remove_widget(name);
                that.add_widget(widget);
            }
        });
    };
};
