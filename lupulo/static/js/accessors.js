(function(){
    var accessors = {};

    // Register an accessor
    register_accessor = function(type, accessor){
        if(type in accessors){
            var type_s = "<strong>" + type + "</strong>";
            add_alert("warning", type_s + " was already registered as an accesor.");
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
                var type_s = "<strong>" + description[i].type + "</strong>";
                add_alert("danger", "Accessor " + type_s + " is not registered");
            }
        }

        // Returns as much function accessors as defined in the description
        return ret;
    }
})();

var jdata_null_msg = "The jdata for the accessor was null, you should " +
                     "check in your widget paint function that you check " +
                     "for a null value before calling the accessor.";

// Built-in accessors
register_accessor("index", function(description){
    var ret = [],
        event_source = description.event,
        old = [];

    if("start" in description &&
    "end" in description){
        var start = description.start,
            end = description.end;
        for(var ii = start; ii < end; ii++){
            // Push the default value for the accessor in the list
            old.push(0);
            // Push a closure which wraps the ii index.
            ret.push((function(index){
                // Return the function which access the jdata
                return function (jdata){
                    var old_index = index - start;
                    var event_name = get_complete_event_name(event_source);
                    var event_s = "<strong>" + event_source + "</strong>"
                    if(jdata === null){
                        add_alert('danger', jdata_null_msg);
                        return old;
                    }
                    if(!(event_name in jdata)){
                        return old[old_index];
                    }else if(jdata[event_name].length <= index){
                        add_alert("danger", "The data of " + event_s +
                                  " is not long enough for a layout.");
                        return old[old_index];
                    }
                    old[old_index] = jdata[event_name][index];
                    return old[old_index];
                }
            })(ii));
        }
    }else{
        add_alert("danger", "<strong>Index</strong> accessor definition was incomplete.");
    }

    return ret;
});

register_accessor("dict", function(description){
    var ret = [],
        event_source = description.event,
        old = 0;

    if("key" in description){
        var key = description.key;
        // Push the function that returns the value associated with a key in a
        // JSON object
        ret.push(function(jdata){
            var event_name = get_complete_event_name(event_source);
            var event_s = "<strong>" + event_source + "</strong>"
            if(jdata === null){
                add_alert('danger', jdata_null_msg);
                return old;
            }
            if(!(event_name in jdata)){
                return old;
            }
            if(!(key in jdata[event_name])){
                var key_s = "<strong>" + key + "</strong>";
                add_alert("danger", key_s + " is not in the " + event_s + " dict event source.");
                return old;
            }
            old = jdata[event_name][key];
            return old;
        });
    }else{
        add_alert("danger", "<strong>Dict</strong> accessor definition was incomplete.");
    }

    return ret;
});

register_accessor("primitive", function(description){
    var event_source = description.event;
    var old = 0;

    return [function(jdata){
        var event_name = get_complete_event_name(event_source);
        var event_s = "<strong>" + event_source + "</strong>"
        if(jdata === null){
            add_alert('danger', jdata_null_msg);
            return old;
        }
        if(event_name in jdata){
            old = jdata[event_name];
        }

        return old;
    }];
});
