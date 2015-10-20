// The only way to retrieve a bunch of accessors is through this function
function get_accessors(layout){
    var accessors = {
        // Returns the data associated with a index i of a list
        "index": function(event_name, i){
            return function(jdata){
                return jdata[event_name][i];
            }
        },

        // Accessors used for the motor event
        "speed_accessor": function(n){
            return function(l){
                return l[n].speed;
            }
        },
        "turn_radius_accessor": function(n){
            return function(l){
                return l[n].turn_radius;
            }
        },
    };

    var ret = [],
        accessor,
        description = layout.accessors;
    for(var i = 0; i < description.length; i++){
        if("start" in description[i] &&
        "end" in description[i] &&
        "index" === description[i].type){
            var type = description[i].type,
                start = description[i].start,
                end = description[i].end;
            for(var ii = start; ii < end; ii++){
                accessor = accessors[type](event_name, ii);
                ret.push(accessor);
            }
        }else{
            console.log("[!] Definition for description #" + i + " in " +
                        layout.type + " incomplete.");
        }
    }

    // Returns as much function accessors as defined in the description
    return ret;
}
