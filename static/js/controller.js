(function (){
    function print(name){
        return function(event) {
            element = document.getElementById(name);
            element.innerHTML = name + ": " + event.data;
        };
    };
    eventSource = new EventSource("http://localhost:8080/subscribe");
    eventSource.addEventListener("distances", print("distances"));
    eventSource.addEventListener("leds", print("leds"));
    eventSource.addEventListener("battery", print("battery"));
    eventSource.addEventListener("date", print("date"));
    eventSource.addEventListener("rotation", print("rotation"));
    eventSource.addEventListener("direction", print("direction"));
    eventSource.addEventListener("acceleration", print("acceleration"));
    eventSource.addEventListener("motor", print("motor"));
    pololu = new Pololu();
})();
