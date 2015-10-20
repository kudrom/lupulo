(function(){
    var accessors = {};

    register_accessor = function(type, accessor){
        if(type in accessors){
            console.log("[!] " + type + " was already registered as an accesor.");
        }else{
            accessors[type] = accessor;
        }
    }

    get_accessors = function(description){
        var ret = [],
            accessor,
            parent_accessors,
            child_accessors,
            desc,
            event;
        for(var i = 0; i < description.length; i++){
            var type = description[i].type;
            if(type in accessors){
                // returns a list
                parent_accessors = accessors[type](description[i]);
                if('after' in description[i]){
                    desc = description[i].after;
                    event = description[i].event;
                    for(var iv = 0; iv < desc.length; iv++){
                        desc[iv].event = event;
                    }
                    child_accessors = get_accessors(desc);
                    for(var ii = 0; ii < parent_accessors.length; ii++){
                        for(var iii = 0; iii < child_accessors.length; iii++){
                            ret.push((function (ii, iii){
                                return function(jdata){
                                    var rdata = parent_accessors[ii](jdata);
                                    var complete_event = get_complete_event_name(event);
                                    var child_data = {}
                                    child_data[complete_event] = rdata;
                                    return child_accessors[iii](child_data);
                                }
                            })(ii, iii));
                        }
                    }
                }else{
                    ret = ret.concat(parent_accessors);
                }
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
                        console.log("[!] " + event_source +
                                    " is not an event source of data.");
                        return 0;
                    }else if(jdata[event_name].length <= index){
                        console.log("[!] the data of " + event_source +
                                    " is not long enough for a layout.");
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
                console.log("[!] " + event_source +
                            " is not an event source of data.");
                return 0;
            }else if(!(key in jdata[event_name])){
                console.log("[!] " + key + " is not in the " + 
                            event_source + " dict event source.");
                return 0;
            }
            return jdata[event_name][key];
        });
    }else{
        console.log("[!] Dict accessor definition was incomplete.");
    }

    return ret;
});
