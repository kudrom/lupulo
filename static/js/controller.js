(function (){
    function print(name){
        return function(event) {
            element = document.getElementById(name);
            element.innerHTML = name + ": " + event.data;
        };
    };
    eventSource = new EventSource("http://localhost:8080/subscribe");
    eventSource.addEventListener("id1-distances", print("distances"));
    eventSource.addEventListener("id1-leds", print("leds"));
    eventSource.addEventListener("id1-battery", print("battery"));
    eventSource.addEventListener("id1-date", print("date"));
    eventSource.addEventListener("id1-rotation", print("rotation"));
    eventSource.addEventListener("id1-direction", print("direction"));
    eventSource.addEventListener("id1-acceleration", print("acceleration"));
    eventSource.addEventListener("id1-motor", print("motor"));
    eventSource.addEventListener("id1-floor", print("floor"));

    /*
    var battery = new MultipleLine([0, 100], 100, ["battery"]);
    eventSource.addEventListener("id1-battery", battery.async_callback());

    var distances = new MultipleLine([0, 4], 100, ["a","b","c","d","e","f","g","h"]);
    eventSource.addEventListener("id1-distances", distances.async_callback());
    */
    var rotations1 = new MultipleLine([0, 360], 100, ["a"]);
    eventSource.addEventListener("id1-rotation", rotations1.async_callback());

    var rotations2 = new MultipleLine([0, 360], 100, ["a", "b"]);
    eventSource.addEventListener("id1-rotation", rotations2.async_callback());

    var rotations3 = new MultipleLine([0, 360], 100, ["a","b","c"]);
    eventSource.addEventListener("id1-rotation", rotations3.async_callback());
})();
