DigitalDate = function(layout){
    validate_requirements(['format'], layout);

    // Clone the layout to avoid its pollution
    var layout = jQuery.extend(true, {}, layout);

    // Get the accessor before overwriting it
    this.date_accessor = get_accessors(layout.accessors)[0];

    // Cook the layout for the DigitalDisplay widget
    var splitted_format = layout.format.split("/");
    var total_digits = splitted_format.reduce((acc, x) => acc + x.length, 0);
    layout.digits = splitted_format.map((x) => x.length);
    var event_name = layout.event_names[0];
    layout.accessors = [{
        'type': 'index',
        'start': 0,
        'end': total_digits,
        'event': event_name
    }];
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

            // Build the data that the digital display is going to show
            var data_display = [];
            for(var i = 0; i < splitted_format.length; i++){
                if(splitted_format[i] === 'YYYY'){
                    data_display = data_display.concat(year);
                }else if(splitted_format[i] === 'DD'){
                    data_display = data_display.concat([day / 10 | 0,
                                                        day % 10]);
                }else if(splitted_format[i] === 'MM'){
                    data_display = data_display.concat([month / 10 | 0,
                                                        month % 10]);
                }else if(splitted_format[i] === ''){
                    continue;
                }else{
                    data_display = [];
                    add_alert("warning", "Invalid format for the digital_date" +
                                         " layout with format " + layout.format);
                    break;
                }
            }

            if(data_display.length > 0){
                var event_source = Object.keys(jdata)[0];

                var jdata_display = {};
                jdata_display[event_source] = data_display;

                // Paint the cooked jdata_display
                this.old_paint(jdata_display);
            }
        }
    };

    // Callback from the framework that should leave the widget in a stable
    // state
    this.clear_framebuffers = function(){
        this.old_clear();
    };
};

lupulo_controller.register_widget("digital_date", DigitalDate);
