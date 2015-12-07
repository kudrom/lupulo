Battery = function(layout){
    // Clone the layout to avoid its pollution
    var layout = jQuery.extend(true, {}, layout);

    // The first layout object is used to construct the drawing of the battery.
    // The viewBox is modified to fit the original size of the drawing and
    // avoid some cropping effects.
    layout.viewBox = "0 90 570 350";

    var scale = 1;
    // The size is shared between the drawing of the battery and its display.
    if('width' in layout.size){
        scale = layout.size.width / 320;
        layout.size.width *= 0.4;
        if(!('height' in layout.size)){
            layout.size.height = layout.size.width * 0.7;
        }
    }else if('height' in layout.size){
        scale = layout.size.height / 90;
        layout.size.width = layout.size.height * (10 / 7);
    }

    // The div created below with the id of the widget is going to be removed by
    // the controller when some change is received in its layout, so the two
    // sub-widgets must be children of this div.
    $(layout.anchor).append('<div id="' + layout.name + '"></div>');
    // The battery_display is going to be the anchor of the display.
    $('#' + layout.name).append('<span id="battery-display"></span>');
    // Now change the anchor and the name of the battery drawing to fit the new
    // structure
    layout.anchor = '#' + layout.name;
    layout.name = layout.name + '-pile';

    // Call the SuperType with the information of the drawing of the battery
    Widget.call(this, layout);

    this.accessor = get_accessors(layout.accessors)[0];

    // SVG parts of the drawing of the battery
    var bottle = '<path class="bottle" d="M471.108,96.392H36.27c-20,0-36.27,16.227-36.27,36.172v304.033c0,19.945,16.27,36.172,36.27,36.172h434.838c20,0,36.271-16.227,36.271-36.172V132.564C507.382,112.619,491.108,96.392,471.108,96.392z"/>';
    var lid = '<path class="bottle" d="M532.887,174.891c0,0-1.605,0-3.592,0s-3.592,2.727-3.592,6.086v207.199c0,3.361,1.605,6.086,3.592,6.086h3.592c20,0,36.27-16.227,36.27-36.172V211.063C569.16,191.118,552.887,174.891,532.887,174.891z"/>';
    var bar = '<path d="M126.911,422.065c0,11.455-9.315,20.746-20.802,20.746H53.544c-11.49,0-20.802-9.291-20.802-20.746v-274.97c0-11.459,9.314-20.747,20.802-20.747h52.564c11.491,0,20.802,9.287,20.802,20.747V422.065z"/>';

    // Remember that the svg points to layout.name + '-pile'
    var html_text = bottle + lid;
    this.svg.html(html_text);

    // Just to not have a magic number
    var N_SEGMENTS_BATTERY = 4;

    // This second layout is cooked to the display, this is normal stuff when
    // using DigitalDisplay
    var event_name = layout.event_names[0];
    layout.name = 'battery-display-widget'
    layout.accessors = [{'type': 'index', 'start': 0, 'end': 3, 'event': event_name}]
    // See above to understand why the anchor is changed
    layout.anchor = '#battery-display';
    layout.digits = [3];
    layout.separator = false;
    // Delete this property inherited from the layout of the drawing
    delete layout.viewBox;
    // Use default aspect ratio for the display
    delete layout.size.width;
    layout.size.height = 100 * scale;
    this.display = new DigitalDisplay(layout);

    this.paint = function(jdata){
        if(jdata !== null){
            var level = this.accessor(jdata);
            var thresholds = [15, 50, 75, 90];

            // Calculate the new data for the drawing
            var data = [];
            for(var i = 0; i < N_SEGMENTS_BATTERY; i++){
                if(level >= thresholds[i])
                    data.push(true);
            }

            // Update the bars of the drawing
            var bars = this.svg.selectAll('.bar').data(data);
            bars.exit().remove();
            bars.enter()
                .append('g')
                    .attr('class', 'bar')
                    .html(bar)
                    .attr('transform', function(d, i){
                         return 'translate(' + i*115 + ')';
                    });

            // Light up the drawing
            if(level > thresholds[0]){
                this.svg.selectAll('.bottle').classed('lit', true);
                this.svg.selectAll('.bottle').classed('danger', false);
            }else{
                this.svg.selectAll('.bottle').classed('lit', false);
                this.svg.selectAll('.bottle').classed('danger', true);
            }

            // Calculate the data for the display and draw it
            var data_display = [];
            if(level == 100){
                data_display [1, 0, 0];
            }else{
                data_display.push(0);
                data_display.push(Math.floor(level / 10));
                data_display.push(Math.floor(level % 10));
            }

            var event_source = Object.keys(jdata)[0];
            var jdata_display = {};
            jdata_display[event_source] = data_display;

            this.display.paint(jdata_display);
        }
    };

    this.clear_framebuffers = function(){
        this.svg.selectAll('.bottle').classed('lit', false);
        this.svg.selectAll('.bar').remove();
        this.display.clear_framebuffers()
    }
}

lupulo_controller.register_widget("battery", Battery);
