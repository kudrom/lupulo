(function (){
    function new_event_sources(event){
        function print(event){
            return function(data){
                var msg = "<p>" +
                              "<strong>" + event + "</strong>: " +
                              data.data +
                          "</p>";
                $('#'+event).html(msg);
            }
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
        };

        for(var i = 0; i < events_added.length; i++){
            var cb = print(events_added[i]);
            event_sources_callbacks[events_added[i]] = cb;
            if(id !== "----"){
                var event_source = 'id' + id + '-' + events_removed[i];
                bind_event_source(event_source);
            }
        };
    };

    function bind_event_source(event_source){
        var father = $('.event-sources');
        var event_name = event_source.split('-')[1];
        father.append('<div id="' + event_name + '"></div>');
        var cb = event_sources_callbacks[event_name];
        pipe.addEventListener(event_source, cb);
    };

    function unbind_event_source(event_source){
        var event_name = event_source.split('-')[1];
        $('#' + event_name).remove();
        var cb = event_sources_callbacks[event_name];
        pipe.removeEventListener(event_source, cb);
    }

    function new_devices(event){
        var list = JSON.parse(event.data);
        // If a new device is tracked, show it in the select form
        var device_selector = document.getElementById("device");
        for(var i = 0; i < list.length; i++){
            var option = document.createElement("option");
            option.text = list[i];
            device_selector.add(option);
        };
    };

    function new_widgets(event){

    };

    var pipe = new EventSource("/subscribe"),
        old_id = '----',
        event_sources_callbacks = {};

    pipe.addEventListener("new_widgets", new_widgets);
    pipe.addEventListener("new_devices", new_devices);
    pipe.addEventListener("new_event_sources", new_event_sources);

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
        };
        old_id = id;
    });
})();
