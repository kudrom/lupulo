DigitalDate = function(layout){
    // Clone the layout to avoid its pollution
    var layout = jQuery.extend(true, {}, layout);

    // Get the accessor before overwriting it
    this.date_accessor = get_accessors(layout.accessors)[0];

    // Cook the layout for the DigitalDisplay widget
    var event_name = layout.event_names[0];
    layout.accessors = [{'type': 'index', 'start': 0, 'end': 8, 'event': event_name}];
    layout.digits = [2, 2, 4];
    layout.separator = false;

    // Inherit from DigitalDisplay
    DigitalDisplay.call(this, layout);

    // Store the functions of DigitalDisplay
    this.old_paint = this.paint;
    this.old_clear = this.clear_framebuffers;

    // Callback from the framework
    this.paint = function(jdata){
        if(jdata !== null){
            // Get the raw data
            var date = this.date_accessor(jdata);

            // Cook the jdata for the DigitalDisplay
            var date_obj = new Date(date*1000);
            var day = date_obj.getDate();
            var month = date_obj.getMonth() + 1;
            var year = date_obj.getFullYear().toString().split("").map((x) => parseInt(x));

            var data_display = [day / 10 | 0, day % 10,
                                month / 10 | 0, month % 10]
            data_display = data_display.concat(year);
            var event_source = Object.keys(jdata)[0];

            var jdata_display = {};
            jdata_display[event_source] = data_display;

            // Paint the cooked jdata_display
            this.old_paint(jdata_display);
        }
    };

    // Callback from the framework that should leave the widget in a stable
    // state
    this.clear_framebuffers = function(){
        this.old_clear();
    };
};

lupulo_controller.register_widget("digital_date", DigitalDate);
