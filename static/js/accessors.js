function get_accessor(description){
    // Returns a function accessor that matches the description
    // The description is a list with the list argument the name
    // and the rest the args for the accessor function
    var name = description[0];
    var args = description.splice(1);
    return accessors[name].apply(window, args);
}

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
