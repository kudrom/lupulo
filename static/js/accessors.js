(function(){
    var accessors = {};

    // Register an accessor
    register_accessor = function(type, accessor){
        if(type in accessors){
            console.log("[!] " + type + " was already registered as an accesor.");
        }else{
            accessors[type] = accessor;
        }
    }

    // Given a description of the accessors usually in the layout, return a 
    // list with all the accessors properly described.
    get_accessors = function(description){
        var parent_accessors,
            child_accessors,
            desc,
            event;

        var ret = {};
        if(description instanceof Array){
            ret = [];
        }

        // Iterate over the entire description list
        for(var i in description){
            var type = description[i].type;
            // If the accessor is registered
            if(type in accessors){
                // Construct the accessor of the current description
                parent_accessors = accessors[type](description[i]);
                // If the accessor is part of a chain
                if('after' in description[i]){
                    // Construct a descripiton for the child
                    var partial_ret = [];
                    desc = description[i].after;
                    event = description[i].event;
                    for(var ii = 0; ii < desc.length; ii++){
                        desc[ii].event = event;
                    }
                    // Call recursively with the child definition
                    child_accessors = get_accessors(desc);
                    // Iterate over the parent and child to combine the
                    // accessors with a closure that does the composition of two
                    // accessors
                    for(var pi in parent_accessors){
                        for(var ci in child_accessors){
                            // Encapsulate the closure with the indexes of the
                            // parent and child accessors
                            partial_ret.push((function (pi, ci){
                                return function(jdata){
                                    // Get the data from the parent
                                    var rdata = parent_accessors[pi](jdata);

                                    // If rdata is some primitive data
                                    if(!(rdata instanceof Object)){
                                        return rdata;
                                    }

                                    // Construct the child data
                                    var child_data = {}
                                    var complete_event = get_complete_event_name(event);
                                    child_data[complete_event] = rdata;

                                    // Return the data returned by the child
                                    return child_accessors[ci](child_data);
                                }
                            })(pi, ci));
                        }
                    }

                    if(description instanceof Array){
                        ret = ret.concat(partial_ret);
                    }else{
                        ret[i] = partial_ret;
                    }
                }else{
                    if(description instanceof Array){
                        ret = ret.concat(parent_accessors);
                    }else{
                        ret[i] = parent_accessors;
                    }
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
        // Push the function that returns the value associated with a key in a
        // JSON object
        ret.push(function(jdata){
            var event_name = get_complete_event_name(event_source);
            if(!(event_name in jdata)){
                console.log("[!] " + event_source +
                            " is not an event source of data.");
                return 0;
            }
            if(!(key in jdata[event_name])){
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

register_accessor("primitive", function(description){
    var event_source = description.event;

    return [function(jdata){
        var event_name = get_complete_event_name(event_source);
        if(!(event_name in jdata)){
            console.log("[!] " + event_name +
                        " is not an event source of data.");
            return 0;
        }

        return jdata[event_name];
    }];
});
