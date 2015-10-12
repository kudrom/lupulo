function get_accessor(description){
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
