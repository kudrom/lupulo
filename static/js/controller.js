(function (){
    var ev;
    var data_pipe = new EventSource("http://localhost:8080/subscribe");

    function print(name){
        return function(event) {
            element = document.getElementById(name);
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

    var rotations1 = new MultipleLine([0, 360], 100, ["a"], "Rotation");
    ev = data_pipe.addEventListener("id1-rotation", rotations1.async_callback());
    rotations1.eventListener = ev;

    var rotations2 = new MultipleLine([0, 360], 100, ["aiasdfasdf", "b"], "Rotation");
    ev = data_pipe.addEventListener("id1-rotation", rotations2.async_callback());
    rotations2.eventListener = ev;

    var rotations3 = new MultipleLine([0, 360], 100, ["aaaaaaaaaaaaaaaaab","b","c"], "Rotation");
    ev = data_pipe.addEventListener("id1-rotation", rotations3.async_callback());
    rotations3.eventListener = ev;
})();
