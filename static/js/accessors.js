(function(){
    var accessors = {};

    register_accessor = function(type, accessor){
        if(type in accessors){
            console.log("[!] " + type + " was already registered as an accesor.");
        }else{
            accessors[type] = accessor;
        }
    }

    get_accessors = function(layout){
        var ret = [],
            accessor,
            description = layout.accessors;
        for(var i = 0; i < description.length; i++){
            var type = description[i].type;
            if(type in accessors){
                ret = ret.concat(accessors[type](description[i]));
            }else{
                console.log("[!] Accessor " + description[i] + " is not registered");
            }
        }

        // Returns as much function accessors as defined in the description
        return ret;
    }
})();

// Built-in accessors
register_accessor("index", function(description){
    var ret = [],
        event_source = description.event;

    if("start" in description &&
    "end" in description){
        var start = description.start,
            end = description.end;
        for(var ii = start; ii < end; ii++){
            // Push a closure which wraps the ii index.
            ret.push((function(index){
                // Return the function which access the jdata
                return function (jdata){
                    var event_name = get_complete_event_name(event_source);
                    if(!(event_name in jdata)){
                        // TODO: better messages
                        console.log("[!] " + event_name + " not in the data.");
                        return 0;
                    }else if(jdata[event_name].length <= index){
                        console.log("[!] the data list is not long enough.");
                        return 0;
                    }
                    return jdata[event_name][index];
                }
            })(ii));
        }
    }else{
        console.log("[!] Index accessor definition was incomplete.");
    }

    return ret;
});

register_accessor("dict", function(description){
    var ret = [],
        event_source = description.event;

    if("key" in description){
        var key = description.key;
        ret.push(function(jdata){
            var event_name = get_complete_event_name(event_source);
            if(!(event_name in jdata)){
                // TODO: better messages
                console.log("[!] " + event_name + " not in the data.");
                return 0;
            }else if(!(key in jdata[event_name])){
                console.log("[!] " + key + " not in the data.");
                return 0;
            }
            return jdata[event_name][key];
        });
    }else{
        console.log("[!] Dict accessor definition was incomplete.");
    }

    return ret;
});
