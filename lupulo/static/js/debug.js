(function (){
    function pretty(obj, spaces_n, print_indexes){
        var spaces = "";
        for(var i = 0; i < spaces_n ; i++){
            spaces += " ";
        }

        var msg = "";
        var n_keys = 1;
        if(obj instanceof Array){
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

    function new_event_sources(event){
        function print(event){
            return function(data){
                var msg = "<p>" +
                              "<strong>" + event + "</strong>: " +
                              pretty(JSON.parse(data.data), 0, true) +
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
                var event_source = get_complete_event_name(events_removed[i]);
                unbind_event_source(event_source);
            }
            delete event_sources_callbacks[events_removed[i]];
        }

        for(var i = 0; i < events_added.length; i++){
            var cb = print(events_added[i]);
            event_sources_callbacks[events_added[i]] = cb;
            if(id !== "----"){
                var event_source = get_complete_event_name(events_added[i]);
                bind_event_source(event_source);
            }
        }
    };

    function bind_event_source(event_source){
        var father = $('.event-sources');
        var event_name = get_event_name(event_source);
        father.append('<div id="' + event_name + '"></div>');
        var cb = event_sources_callbacks[event_name];
        lupulo_controller.data_pipe.addEventListener(event_source, cb);
    };

    function unbind_event_source(event_source){
        var event_name = get_event_name(event_source);
        $('#' + event_name).remove();
        var cb = event_sources_callbacks[event_name];
        lupulo_controller.data_pipe.removeEventListener(event_source, cb);
    };

    function update_data_panel(widget_name){
        var widget_name = widget_name;
        return function(event){
            var event_name = get_event_name(event.type);
            var panel = $('#' + widget_name + '-wrapper .data-panel');
            var accessors_panel = $('#' + widget_name + '-wrapper .accessors-panel');

            var obj = data_panel_objects[widget_name];
            obj[event_name] = JSON.parse(event.data);

            panel.html(pretty(obj, 0, true));

            obj = {};
            var widget_accessors = accessors[widget_name];
            for(var accessor_index in widget_accessors){
                var jdata = JSON.parse(event.data);
                var fdata = {};
                fdata[event.type] = jdata;
                var accessor = widget_accessors[accessor_index];
                obj[accessor_index] = accessor(fdata);
            }
            accessors_panel.html(pretty(obj, 0, true));
        };
    };

    function new_widgets(event){
        var obj = JSON.parse(event.data),
            widgets_removed = [],
            widgets_added = [];

        if('added' in obj){
            for(var name in obj.added){
                var anchor = obj.added[name].anchor.slice(1)
                var layout = pretty(obj.added[name], 0, false);
                var child = '<div class="clearfix wrapper" id="' + name + '-wrapper">' +
                                '<div class="pull-left">' +
                                    '<pre class="section layout">' +
                                        '<div class="title">Layout</div>' +
                                        layout +
                                    '</pre>' +
                                    '<div class="section">' +
                                        '<div class="title">Raw data</div>' +
                                        '<pre class="data-panel">{}</pre>' +
                                    '</div>' +
                                    '<div class="section">' +
                                        '<div class="title">Accessors data</div>' +
                                        '<pre class="accessors-panel"></pre>' +
                                    '</div>' +
                                '</div>' +
                                '<div class="pull-left widget" id="' + anchor + '">' +
                                    '<div class="title">Widget</div>' +
                                '</div>' +
                            '</div>';
                $('.widgets').append(child);
                var cb = update_data_panel(name);
                data_panel_objects[name] = {};
                data_panel_callbacks[name] = cb;
                data_panel_events[name] = obj.added[name].event_names;
                accessors[name] = get_accessors(obj.added[name].accessors);
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
        event_sources_callbacks = {},
        data_panel_callbacks = {},
        data_panel_events = {},
        data_panel_objects = {},
        accessors = {};

    var device_selector = document.getElementById("device");
    device_selector.addEventListener("change", function(event){
        var id = device_selector.value;
        for(var event_name in event_sources_callbacks){
            if(id === '----'){
                if(old_id !== "----"){
                    var event_source = 'id' + old_id + '-' + event_name;
                    unbind_event_source(event_source);
                }
            }else{
                var event_source = get_complete_event_name(event_name);
                bind_event_source(event_source);
            }
        }

        for(var widget_name in data_panel_callbacks){
            var events = data_panel_events[widget_name];
            if(id === '----'){
                if(old_id !== "----"){
                    for(var i = 0; i < events.length; i++){
                        var event_source = 'id' + old_id + '-' + events[i];
                    }
                }
            }else{
                for(var i = 0; i < events.length; i++){
                    var event_source = get_complete_event_name(events[i]);
                    var cb = data_panel_callbacks[widget_name];
                    lupulo_controller.data_pipe.addEventListener(event_source ,cb);
                }
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
