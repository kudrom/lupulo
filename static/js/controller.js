(function (){
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

    // Callback for the housekeeping data event source
    function housekeeping(event){
        var obj = JSON.parse(event.data);
        // If a new robot is tracked, show it in the select form
        if("added_robots" in obj){
            var select_element = document.getElementById("robot");
            for(var i = 0; i < obj["added_robots"].length; i++){
                var option = document.createElement("option");
                option.text = obj["added_robots"][i];
                select_element.add(option);
            }
        }
    };

    // Add widget to the widgets dictionary and bind it to the data_pipe EventSource
    function add_widget(widget, source_event){
        var iid = robot_selector.value === "" ? 1 : robot_selector.value;
        var complete_event_name = "id" + iid + "-" + source_event;
        if(!(complete_event_name in widgets)){
            widgets[complete_event_name] = [];
        }
        widgets[complete_event_name].push(widget);
        data_pipe.addEventListener(complete_event_name, widget.async_callback);
    }

    // Remove widget to the widgets dictionary and unbind it to the data_pipe EventSource
    function remove_widget(widget, event_name){
        var i = widgets[event_name].indexOf(widget);
        widgets[event_name].splice(i, 1);
        if(widgets[event_name].length == 0){
            delete widgets[event_name];
        }
        data_pipe.removeEventListener(event_name, widget.async_callback);
    }

    // Dictionary which stores all the widgets in the page indexed by the name of the 
    // tracked event
    var widgets = {};

    // Client SSE to access the information from the backend 
    var data_pipe = new EventSource("/subscribe");
    data_pipe.addEventListener("housekeeping", housekeeping);

    // When the #robot changes, all widgets should be refreshed with the new robot id
    var robot_selector = document.getElementById("robot");
    robot_selector.addEventListener("change", function(){
        for(var event_name in widgets){
            var len = widgets[event_name].length;
            for(var i = 0; i < len; i++){
                var last_index = widgets[event_name].length -1;
                var widget = widgets[event_name][last_index];
                widget.clear_framebuffers();
                remove_widget(widget, event_name);
                // Bind the widget to the new robot id
                var source_event = event_name.split("-")[1];
                add_widget(widget, source_event);
            }
        }
    });


    // Accessor function for the layouts of the widgets
    function index(i){
        return function(list){
            return list[i];
        }
    }

    // Creation of widgets
    var layout = {
        size: {width: 960, height: 500},
        seconds: 100
    };

    layout.range = [0, 100];
    layout.name_lines = ["Battery"];
    layout.y_name = "Battery";
    layout.accessors = [index(0)];
    var battery = new MultipleLine(layout);
    add_widget(battery, "battery");

    layout.range = [0, 4];

    layout.name_lines = ["Front-left", "Front-center", "Front-right"];
    layout.y_name = "Distances front";
    layout.accessors = [index(0), index(1), index(2)];
    var distances1 = new MultipleLine(layout);
    add_widget(distances1, "distances");

    layout.name_lines = ["Middle-left", "Middle-right"];
    layout.y_name = "Distances middle";
    layout.accessors = [index(3), index(4)];
    var distances2 = new MultipleLine(layout);
    add_widget(distances2, "distances");

    layout.name_lines = ["Back-left", "Back-center", "Back-right"];
    layout.y_name = "Distances back";
    layout.accessors = [index(5), index(6), index(7)];
    var distances3 = new MultipleLine(layout);
    add_widget(distances3, "distances");


    layout.name_lines = ["x", "y", "z"];
    layout.y_name = "Rotation";
    layout.accessors = [index(0), index(1), index(2)];
    layout.range = [0, 360];
    var rotations = new MultipleLine(layout);
    add_widget(rotations, "rotation");


    layout.name_lines = ["x", "y", "z"];
    layout.y_name = "Acceleration";
    layout.accessors = [index(0), index(1), index(2)];
    layout.range = [0, 10];
    var acceleration = new MultipleLine(layout);
    add_widget(acceleration, "acceleration");


    layout.name_lines = ["floor1", "floor2", "floor3", "floor4"];
    layout.y_name = "Floor";
    layout.accessors = [index(0), index(1), index(2), index(3)];
    layout.range = [0, 5];
    var floor = new MultipleLine(layout);
    add_widget(floor, "floor");


    function speed_accessor(n){
        return function(l){
            return l[n].speed;
        }
    }

    layout.name_lines = ["speed-left", "speed-right"];
    layout.y_name = "Speed";
    layout.accessors = [speed_accessor(0), speed_accessor(1)];
    layout.range = [0, 5];
    var speed = new MultipleLine(layout);
    add_widget(speed, "motor");


    function turn_radius_accessor(n){
        return function(l){
            return l[n].turn_radius;
        }
    }

    layout.name_lines = ["turn-radius-left", "turn-radius-right"];
    layout.y_name = "Turn radius";
    layout.accessors = [turn_radius_accessor(0), turn_radius_accessor(1)];
    layout.range = [0, 3];
    var turn_radius = new MultipleLine(layout);
    add_widget(turn_radius, "motor");

})();
