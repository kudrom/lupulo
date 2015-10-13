// The only way to retrieve a bunch of accessors is through this function
function get_accessors(description){
    var accessors = {
        // Returns the data associated with a index i of a list
        "index": function(i){
            return function(list){
                return list[i];
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
        accessor;
    for(var i = 0; i < description.length; i++){
        if("start" in description[i] && "end" in description[i] && "name" in description[i]){
            var name = description[i].name,
                start = description[i].start,
                end = description[i].end;
            for(var ii = start; ii < end; ii++){
                accessor = accessors[name](ii);
                ret.push(accessor);
            }
        }else{
            console.log("[!] Definition for description #" + i + " incomplete.");
        }
    }

    // Returns as much function accessors as defined in the description
    return ret;
}
