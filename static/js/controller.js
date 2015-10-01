function debug(data_pipe){
    function print(name){
        return function(event) {
            var element = document.getElementById(name);
            element.innerHTML = name + ": " + event.data;
        };
    };
    data_pipe.addEventListener("id1-distances", print("distances"));
    data_pipe.addEventListener("id1-leds", print("leds"));
    data_pipe.addEventListener("id1-battery", print("battery"));
    data_pipe.addEventListener("id1-date", print("date"));
    data_pipe.addEventListener("id1-rotation", print("rotation"));
    data_pipe.addEventListener("id1-direction", print("direction"));
    data_pipe.addEventListener("id1-acceleration", print("acceleration"));
    data_pipe.addEventListener("id1-motor", print("motor"));
    data_pipe.addEventListener("id1-floor", print("floor"));
}

(function (){
    function housekeeping(event){
        var obj = JSON.parse(event.data);
        if("added_robots" in obj){
            var selector = document.getElementById("robot");
            for(var i = 0; i < obj["added_robots"].length; i++){
                var item = document.createElement("option");
                item.text = obj["added_robots"][i];
                selector.add(item);
            }
        }
    };

    var widgets = [];
    var data_pipe = new EventSource("http://localhost:8080/subscribe");
    data_pipe.addEventListener("housekeeping", housekeeping);

    //debug(data_pipe);

    var listener;
    var rotations1 = new MultipleLine([0, 360], 100, ["a"], "Rotation");
    listener = data_pipe.addEventListener("id1-rotation", rotations1.async_callback());
    rotations1.eventListener = listener;

    var rotations2 = new MultipleLine([0, 360], 100, ["aiasdfasdf", "b"], "Rotation");
    listener = data_pipe.addEventListener("id1-rotation", rotations2.async_callback());
    rotations2.eventListener = listener;

    var rotations3 = new MultipleLine([0, 360], 100, ["aaaaaaaaaaaaaaaaab","b","c"], "Rotation");
    listener = data_pipe.addEventListener("id1-rotation", rotations3.async_callback());
    rotations3.eventListener = listener;
})();
