DigitalClock = function(layout){
    // Clone the layout to avoid its pollution
    var layout = jQuery.extend(true, {}, layout);

    // Check the requirements
    validate_requirements(['device_time'], layout);

    // Get the accessor before overwriting it
    this.clock_accessor = get_accessors(layout.accessors)[0];

    // Cook the layout for the DigitalDisplay widget
    var event_name = layout.event_names[0];
    layout.accessors = [{'type': 'index', 'start': 0, 'end': 6, 'event': event_name}];
    layout.digits = [2, 2, 2];
    layout.separator = true;

    // Inherit from DigitalDisplay
    DigitalDisplay.call(this, layout);

    // Store the functions of DigitalDisplay
    this.old_paint = this.paint;
    this.old_clear = this.clear_framebuffers;

    // Callback from the framework
    this.paint = function(jdata){
        // Print the current time each second
        if(!layout.device_time){
            var event_source = get_complete_event_name(event_name);
            var jdata = {};
            jdata[event_source] = (new Date().getTime()) / 1000;
        }

        if(jdata !== null){
            // Get the raw date
            var date = this.clock_accessor(jdata);

            // Cook the jdata for DigitalDisplay
            var date_obj = new Date(date*1000);
            var hours = date_obj.getHours();
            var minutes = date_obj.getMinutes();
            var seconds = date_obj.getSeconds();

            var data_display = [hours / 10 | 0, hours % 10,
                                minutes / 10 | 0, minutes % 10,
                                seconds / 10 | 0, seconds % 10];
            var event_source = Object.keys(jdata)[0];

            var jdata_display = {};
            jdata_display[event_source] = data_display;

            // Render the jdata_display
            this.old_paint(jdata_display);
        }
    };

    // Callback from the framework that should leave the widget in a stable
    // state
    this.clear_framebuffers = function(){
        this.old_clear();
    };
};

lupulo_controller.register_widget("digital_clock", DigitalClock);
