(function (){
    function new_event_sources(event){
        function print(event){
            return function(data){
                var msg = "<p>" +
                              "<strong>" + event + "</strong>: " +
                              data.data +
                          "</p>";
                $('#'+event).html(msg);
            };
        };

        var obj = JSON.parse(event.data),
            events_removed = obj.removed,
            events_added = obj.added,
            device_selector = document.getElementById("device"),
            id = device_selector.value;

        for(var i = 0; i < events_removed.length; i++){
            if(id !== "----"){
                var event_source = 'id' + id + '-' + events_removed[i];
                unbind_event_source(event_source);
            }
            delete event_sources_callbacks[events_removed[i]];
        }

        for(var i = 0; i < events_added.length; i++){
            var cb = print(events_added[i]);
            event_sources_callbacks[events_added[i]] = cb;
            if(id !== "----"){
                var event_source = 'id' + id + '-' + events_added[i];
                bind_event_source(event_source);
            }
        }
    };

    function bind_event_source(event_source){
        var father = $('.event-sources');
        var event_name = event_source.split('-')[1];
        father.append('<div id="' + event_name + '"></div>');
        var cb = event_sources_callbacks[event_name];
        lupulo_controller.data_pipe.addEventListener(event_source, cb);
    };

    function unbind_event_source(event_source){
        var event_name = event_source.split('-')[1];
        $('#' + event_name).remove();
        var cb = event_sources_callbacks[event_name];
        lupulo_controller.data_pipe.removeEventListener(event_source, cb);
    };

    function new_widgets(event){
        var obj = JSON.parse(event.data),
            widgets_removed = [],
            widgets_added = [];

        if('added' in obj){
            for(var event_name in obj.added){
                var anchor = obj.added[event_name].anchor.slice(1)
                var child = '<div id="' + event_name + '-wrapper">' +
                                '<div id="' + anchor + '"></div>' +
                            '</div>';
                $('.widgets').append(child);
            }
        }

        if('removed' in obj){
            for(var i = 0; i < obj.removed.length; i++){
                $('#wrapper-' + obj.removed[i]).remove();
            }
        }

        lupulo_controller.new_widgets(event);
    };

    var old_id = '----',
        event_sources_callbacks = {};

    var device_selector = document.getElementById("device");
    device_selector.addEventListener("change", function(event){
        var id = device_selector.value;
        for(var event_name in event_sources_callbacks){
            if(id === '----'){
                if(old_id !== "----"){
                    unbind_event_source(event_source);
                }
            }else{
                var event_source = 'id' + id + '-' + event_name;
                bind_event_source(event_source);
            }
        }
        for(var name in lupulo_controller.widgets){
            widget = lupulo_controller.widgets[name];
            widget.clear_framebuffers();
            lupulo_controller.remove_widget(name);
            lupulo_controller.add_widget(widget);
        }
        old_id = id;
    });

    lupulo_controller = new Controller();
    lupulo_controller.setup();
    lupulo_controller.data_pipe.addEventListener("new_widgets", new_widgets);
    lupulo_controller.data_pipe.addEventListener("new_devices", lupulo_controller.new_devices);
    lupulo_controller.data_pipe.addEventListener("new_event_sources", new_event_sources);
})();
