DigitalDisplay = function(layout){
    // Requirements for the layout
    validate_requirements(['digits', 'separator'], layout);

    // Calculate the sizes and the scales for the given layout.size
    var digit_size = 52;
    var separator_size = 20;
    var num_separators = layout.digits.length - 1;
    var num_digits = layout.digits.reduce((prev, curr) => prev + curr);
    var total_width = num_digits * digit_size + num_separators * separator_size;
    var total_height = 100;
    var scalex = 1;
    var scaley = 1;

    // If both width and height are in the layout, the aspect ratio can be
    // violated with the new scales, otherwise the height or width are fixed
    // to keep the aspect ratio.
    if('width' in layout.size && 'height' in layout.size){
        scalex = layout.size.width / total_width;
        scaley = layout.size.height / total_height;
    }else if('width' in layout.size){
        scalex = layout.size.width / total_width;
        scaley = scalex;
        layout.size.height = scalex * total_height;
    }else if('height' in layout.size){
        scaley = layout.size.height / total_height;
        scalex = scaley;
        layout.size.width = scaley * total_width;
    }

    // Inherit from Widget
    Widget.call(this, layout);

    // Get the accessors from the layout definition
    this.accessors = get_accessors(layout.accessors);

    // Seven segments for the display
    var digit_paths = `
<path d="M10,8L14,4L42,4L46,8L42,12L14,12L10,8z"/>
<path d="M8,10L12,14L12,42L8,46L4,42L4,14L8,10z"/>
<path d="M48,10L52,14L52,42L48,46L44,42L44,14L48,10z"/>
<path d="M10,48L14,44L42,44L46,48L42,52L14,52L10,48z"/>
<path d="M8,50L12,54L12,82L8,86L4,82L4,54L8,50z"/>
<path d="M48,50L52,54L52,82L48,86L44,82L44,54L48,50z"/>
<path d="M10,88L14,84L42,84L46,88L42,92L14,92L10,88z"/>`;

    // Circles for the separator
    var separator_circles = `
<circle r="4" cx="0" cy="28"/>
<circle r="4" cx="0" cy="68"/>`;

    var separators_amount = 0;
    var previous_digits = 0;
    var total_groups = layout.digits.length;
    var html_text = '<g transform="scale(' + scalex + ' ' + scaley + ')">';
    for(var i = 0; i < total_groups; i++){
        var translation_amount = (digit_size*previous_digits) + separators_amount;

        // Wrapper around each group of digits
        html_text += '<g transform=translate(' + translation_amount + ')>';
        for(var ii = 0; ii < layout.digits[i]; ii++){
            var n = ii * digit_size;
            html_text += '<g class="digit" transform="skewX(0) ' +
                                                     'translate(' + n + ')">';
            html_text += digit_paths;
            html_text += '</g>';
        }
        html_text += '</g>';

        previous_digits += ii;

        // Print separators
        if((i + 1) < total_groups){
            separators_amount += separator_size;
            if(layout.separator){
                var tr = (digit_size*previous_digits) + separators_amount - 8;
                html_text += '<g class="separator" transform=translate(' + tr + ')>';
                html_text += separator_circles;
                html_text += '</g>'
            }
        }
    }
    html_text += '</g>'

    this.svg.html(html_text);

    this.digit = this.svg.selectAll(".digit");
    this.separators = this.svg.selectAll(".separator circle");

    // Each list is a segment of the display, and each element in the list is
    // to set the lit class for each number from 0 to 9
    this.digitPattern = [
      [1,0,1,1,0,1,1,1,1,1],
      [1,0,0,0,1,1,1,0,1,1],
      [1,1,1,1,1,0,0,1,1,1],
      [0,0,1,1,1,1,1,0,1,1],
      [1,0,1,0,0,0,1,0,1,0],
      [1,1,0,1,1,1,1,1,1,1],
      [1,0,1,1,0,1,1,0,1,1]
    ];
    
    // Callback from the framework
    this.paint = function(jdata){
        if(jdata !== null){
            // For the anonymous functions to be able to access it
            var digitPattern = this.digitPattern;

            var data = [];
            for(var i = 0; i < this.accessors.length; i++){
                data.push(this.accessors[i](jdata));
            }
            this.digit = this.digit.data(data);

            // Select in order each segment of every digit and lit it if the
            // number of the digit demands it
            this.digit.select("path:nth-child(1)")
                     .classed("lit", function(d) { return digitPattern[0][d]; });
            this.digit.select("path:nth-child(2)")
                     .classed("lit", function(d) { return digitPattern[1][d]; });
            this.digit.select("path:nth-child(3)")
                     .classed("lit", function(d) { return digitPattern[2][d]; });
            this.digit.select("path:nth-child(4)")
                     .classed("lit", function(d) { return digitPattern[3][d]; });
            this.digit.select("path:nth-child(5)")
                     .classed("lit", function(d) { return digitPattern[4][d]; });
            this.digit.select("path:nth-child(6)")
                     .classed("lit", function(d) { return digitPattern[5][d]; });
            this.digit.select("path:nth-child(7)")
                     .classed("lit", function(d) { return digitPattern[6][d]; });

            // The separators are always turned on
            this.separators.classed("lit", 1);
        }
    };

    // Callback from the framework that should leave the widget in a stable
    // state
    this.clear_framebuffers = function(){
        this.digit.selectAll("path").classed("lit", 0);
        this.separators.classed("lit", 0);
    };
};

// Registration of the widget
lupulo_controller.register_widget("digital_display", DigitalDisplay);
