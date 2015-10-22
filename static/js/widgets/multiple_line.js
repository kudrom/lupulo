MultipleLine = function(layout){
    (function(requirements){
        var broken = false;
        for(var i = 0; i < requirements.length; i++){
            if(!(requirements[i] in layout)){
                console.log(requirements[i] + " not in layout " + layout.name);
                broken = true;
            }
        }
        if(broken){
            throw "Broken preconditions for " + layout.name;
        }
    })(['y_name', 'seconds', 'name_lines', 'accessors']);
    Widget.call(this, layout);

    var Line = function(accessor){
        // Array for the data displayed
        this.framebuffer = [];
        // SVG path of this line
        this.path;
        // The accessor function to return a value associated with a
        // complex jdata object of an event source connection
        this.accessor = accessor;
    }

    // Width of the time scale
    this.seconds = layout.seconds;

    var accessors = get_accessors(layout.accessors);
    if(accessors.length < layout.name_lines.length){
        throw "[!] There are more name_lines than accessors for " + layout.name;
    }else if(accessors.length > layout.name_lines.length){
        console.log("[!] There are more accessors that name_lines for " + layout.name);
    }

    // The Lines present in this graph
    this.lines = [];
    // We use the length of name_lines to not create too much Lines if there are
    // more accessors that name_lines;
    for(var i = 0; i < layout.name_lines.length; i++){
        accessor = accessors[i];
        this.lines.push(new Line(accessor));
    }

    // X axis
    var x = d3.scale.linear()
        .domain([0, this.seconds - 1])
        .range([0, this.width]);
    this.x = x;

    // Y axis
    var y = d3.scale.linear()
        .domain(layout.range)
        .range([this.height, 0]);
    this.y = y;

    // Color scale
    var color = d3.scale.category10()
        .domain(layout.name_lines);

    // Line who renders the control points of the svg path
    this.line = d3.svg.line()
        .x(function(d, ii) { return x(ii - 1); })
        .y(function(d, ii) { return y(d); });

    // The clip is used to avoid rendering of the left control point when
    // it's being moved by the transition
    // The lines have the smallest z-index
    this.svg.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", this.width)
        .attr("height", this.height);

    // Render the x axis
    this.svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3.svg.axis().scale(x).orient("bottom"))
    .append("text")
        .attr("y", -16)
        .attr("x", this.width - 15)
        .attr("dy", "1em")
        .attr("text-anchor", "end")
        .text("Time (s)")

    // Render the y axis
    this.svg.append("g")
        .attr("class", "y axis")
        .call(d3.svg.axis().scale(y).orient("left"))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "1em")
      .style("text-anchor", "end")
      .text(layout.y_name);

    // Render the legends
    var max_name_line = d3.max(layout.name_lines, function(d){return 7 * d.length});
    var width_rect = 15;
    var width_margin = 5;
    var width_legend =  max_name_line + width_rect + width_margin;
    var width = this.width;
    var legend = this.svg.selectAll('.legend')
        .data(color.domain())
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', function(d, ii){
            return 'translate(' + (width - width_legend) + ','
                    + ((width_rect + width_margin) * ii) + ')';
        });
    legend.append('rect')
        .attr('width', width_rect)
        .attr('height', width_rect)
        .style('fill', color)
        .style('stroke', color);
    legend.append('text')
        .attr('x', width_rect + width_margin)
        .attr('y', function(d, ii){return (width_rect - width_margin)})
        .text(function(d){return d;});

    // Bind the svg path to every line displayed in the graph
    for(i = 0; i < layout.name_lines.length; i++){
        this.lines[i].path = this.svg.append("g")
            .attr("clip-path", "url(#clip)")
          .append("path")
            .datum(this.lines[i].framebuffer)
            .attr("class", "line")
            .attr("stroke", function(d){return color(layout.name_lines[i])})
            .attr("d", this.line);
    }

    this.paint = function(jdata){
        var last = 0;
        for(var i = 0; i < this.lines.length; i++){
            if(jdata !== null){
                last = this.lines[i].accessor(jdata);
            }

            // push a new data point onto the front
            this.lines[i].framebuffer.unshift(last);

            // redraw the line, and slide it to the right
            this.lines[i].path
              .attr("d", this.line)
              .attr("transform", null)
            .transition()
              .duration(1000)
              .ease("linear")
              .attr("transform", "translate(" + x(1) + ",0)");

            // pop the old data point off the back
            if(this.lines[i].framebuffer.length == this.seconds + 1){
              this.lines[i].framebuffer.pop();
            }
        }
    }

    // Clear all the framebuffers of the lines associated with the graph
    this.clear_framebuffers = function(){
        for(var i = 0; i < this.lines.length; i++){
            this.lines[i].framebuffer.splice(0, this.lines[i].framebuffer.length);
        }
    }
};

// Register the Klass as a factory for multiple_line widgets
register_widget("multiple_line", MultipleLine);
