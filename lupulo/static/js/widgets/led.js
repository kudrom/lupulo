Led = function(layout){
    validate_requirements(['mapping', 'radius'], layout);

    // Dynamic sizing
    if('height' in layout.size && 'width' in layout.size &&
       layout.size.height != layout.size.width){
        add_alert('warning', 'The width and height for ' + layout.name +
                            ' are not the same, maybe the led will be cropped.');
    }else if('height' in layout.size){
        layout.size.width = layout.size.height;
    }else if('width' in layout.size){
        layout.size.height = layout.size.width;
    }

    Widget.call(this, layout);
    this.accessor = get_accessors(layout.accessors)[0];

    // Center of the led
    var cx = layout.size.width / 2;
    var cy = layout.size.height / 2;

    // The ellipse is going to be in the top left corner
    // With the scale the position is responsive to how big the led is in
    // relation to the entire svg, that way it's always in the same position
    // no matter the size of the led.
    var scale = layout.radius / layout.size.width;
    var ecx = cx * (1 - (scale*0.7));
    var ecy = cy * (1 - (scale*0.7));

    this.mapping = function(data){
        /*
         * This function will return the color in the mapping section in the 
         * layout for a given data.
         */
        var ret = "grey";
        for(key in layout.mapping){
            if(key.indexOf(" to ") !== -1){
                var range = key.split(" to ").map((e) => parseInt(e));
                if(data >= range[0] && data <= range[1]){
                    ret = layout.mapping[key];
                    break;
                }
            }else{
                if(data === key){
                    ret = layout.mapping[key];
                    break;
                }
            }
        }

        return ret;
    };

    this.paint = function(jdata){
        // Change the color if necessary
        var color = "grey";
        if(jdata !== null){
            var data = this.accessor(jdata);

            if(data !== null){
                color = this.mapping(data);
            }

        }

        var gradient_led = this.svg.select('#gradient-led stop');
        gradient_led.attr('stop-color', color);
    };

    this.clear_framebuffers = function(){
        this.paint(null);
    };

    this.svg.append("filter")
        .attr("id", "blur")
        .html('<feGaussianBlur in="SourceGraphic" stdDeviation="2" />');

    this.svg.append("defs")
        .html('<linearGradient id="gradient-led" ' +
                              'x2="250%" ' +
                              'gradientTransform="rotate(45)">' +
                  '<stop offset="0%" stop-color="green" stop-opacity=1 />' +
                  '<stop offset="100%" stop-color="white" stop-opacity=1 />' +
              '</linearGradient>' +
              '<linearGradient id="gradient-glow" ' +
                              'x2="100%" ' +
                              'gradientTransform="rotate(45)">' +
                  '<stop offset="0%" stop-color="white" stop-opacity=1 />' +
                  '<stop offset="100%" stop-color="white" stop-opacity=0.3 />' +
              '</linearGradient>');

    var circle = this.svg.append('circle');
    circle.attr('class', 'led-circle');
    circle.attr('r', layout.radius - 5);
    circle.attr('cx', cx);
    circle.attr('cy', cy);
    circle.attr('filter', 'url(#blur)');

    var ellipse = this.svg.append('ellipse')
    ellipse.attr('rx', layout.radius * 0.63);
    ellipse.attr('ry', layout.radius * 0.36);
    ellipse.attr('cx', ecx);
    ellipse.attr('cy', ecy);
    ellipse.attr('fill', 'url(#gradient-glow)');
    ellipse.attr('fill-opacity', '0.3');
    ellipse.attr('filter', 'url(#blur)');
    ellipse.attr('transform', 'rotate(-45 ' + ecx + ' ' + ecy + ' )');
};

lupulo_controller.register_widget('led', Led);
