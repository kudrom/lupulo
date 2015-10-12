(function (){
    // Callback for the new_robots data event source
    function new_robots(event){
        var list = JSON.parse(event.data);
        // If a new robot is tracked, show it in the select form
        var select_element = document.getElementById("robot");
        for(var i = 0; i < list.length; i++){
            var option = document.createElement("option");
            option.text = list[i];
            select_element.add(option);
        }
    };

    // Callback for the new_widgets data event source
    function new_widgets(event){
        var layouts = JSON.parse(event.data),
            layout,
            widget;
        for(var i = 0; i < layouts.length; i++){
            layout = layouts[i];
            widget = new widget_ctor[layout.type](layout);
            add_widget(widget, layout.event_name);
        }
        console.log(layouts);
    };

    // Add widget to the widgets dictionary and bind it to the data_pipe EventSource
    function add_widget(widget, source_event){
        var iid = robot_selector.value === "" ? "----" : robot_selector.value;
        if(iid[0] !== "-" ){
            var complete_event_name = "id" + iid + "-" + source_event;
            data_pipe.addEventListener(complete_event_name, widget.async_callback);
        }else{
            var complete_event_name = "noid-" + source_event;
        }
        if(!(complete_event_name in widgets)){
            widgets[complete_event_name] = [];
        }
        widgets[complete_event_name].push(widget);
    }

    // Remove widget to the widgets dictionary and unbind it to the data_pipe EventSource
    function remove_widget(widget, event_name){
        var i = widgets[event_name].indexOf(widget);
        widgets[event_name].splice(i, 1);
        if(widgets[event_name].length === 0){
            delete widgets[event_name];
        }
        // If the widget was binded to any real event source (not the noid- virtual event source)
        if(event_name[0] !== "n"){
            data_pipe.removeEventListener(event_name, widget.async_callback);
        }
    }

    // Dictionary which stores all the widgets in the page indexed by the name of the 
    // tracked event
    var widgets = {};
    var widget_ctor = {
        "multiple_line": MultipleLine
    }

    // Client SSE to access the information from the backend 
    var data_pipe = new EventSource("/subscribe");
    data_pipe.addEventListener("new_widgets", new_widgets);
    data_pipe.addEventListener("new_robots", new_robots);

    // When the #robot changes, all widgets should be refreshed with the new robot id
    var robot_selector = document.getElementById("robot");
    robot_selector.addEventListener("change", function(){
        for(var event_name in widgets){
            var len = widgets[event_name].length;
            for(var i = 0; i < len; i++){
                var last_index = widgets[event_name].length -1;
                var widget = widgets[event_name][last_index];
                widget.clear_framebuffers();
                remove_widget(widget, event_name);
                // Bind the widget to the new robot id
                var source_event = event_name.split("-")[1];
                add_widget(widget, source_event);
            }
        }
    });
})();
