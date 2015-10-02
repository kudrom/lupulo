Line = function(name){
    this.last = 0;
    // Array for the data displayed
    this.framebuffer = [];
    // SVG path
    this.path;
}

MultipleLine = function(layout){
    // Width of the time scale
    this.seconds = layout.seconds;
    // The Lines present in this graph
    this.lines = [];
    for(var i = 0; i < layout.name_lines.length; i++){
        this.lines.push(new Line());
    }
    this.accessors = layout.accessors;

    var margin = {top: 20, right: 20, bottom: 20, left: 40},
        width = layout.size.width - margin.left - margin.right,
        height = layout.size.height - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain([0, this.seconds - 1])
        .range([0, width]);
    this.x = x;

    var y = d3.scale.linear()
        .domain(layout.range)
        .range([height, 0]);
    this.y = y;

    var color = d3.scale.category10()
        .domain(layout.name_lines);

    this.line = d3.svg.line()
        .x(function(d, ii) { return x(ii - 1); })
        .y(function(d, ii) { return y(d); });

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Use clip to avoid rendering of the left control point when
    // it's being moved by the transition
    svg.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);

    // The lines have the smallest z-index
    this.container = svg.append("g")
        .attr("class", "container");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.svg.axis().scale(x).orient("bottom"));

    svg.append("g")
        .attr("class", "y axis")
        .call(d3.svg.axis().scale(y).orient("left"))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "1em")
      .style("text-anchor", "end")
      .text(layout.y_name);

    var width_rect = 15;
    var width_margin = 5;
    var width_legend = d3.max(layout.name_lines, function(d){return 7 * d.length}) + width_rect + width_margin;
    var legend = svg.selectAll('.legend')
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

    for(i = 0; i < layout.name_lines.length; i++){
        this.lines[i].path = this.container.append("g")
            .attr("clip-path", "url(#clip)")
          .append("path")
            .datum(this.lines[i].framebuffer)
            .attr("class", "line")
            .attr("stroke", function(d){return color(layout.name_lines[i])})
            .attr("d", this.line);
    }

    this.tick = function(that) {
        for(var i = 0; i < that.lines.length; i++){
            // push a new data point onto the front
            that.lines[i].framebuffer.unshift(that.lines[i].last);

            // redraw the line, and slide it to the right
            that.lines[i].path
              .attr("d", that.line)
              .attr("transform", null)
            .transition()
              .duration(1000)
              .ease("linear")
              .attr("transform", "translate(" + x(1) + ",0)");

            // pop the old data point off the back
            if(that.lines[i].framebuffer.length == that.seconds + 1){
              that.lines[i].framebuffer.pop();
            }
        }

        // BUG #2079, registers the callback through d3js to avoid
        // funky slide movements
        that.container.transition()
          .duration(1000)
          .each("end", function(){that.tick(that)});

    }

    this.async_callback_ctor = function() {
        var that = this;
        this.tick(this);
        return function(event){
            var jdata = JSON.parse(event.data);
            if(!(jdata instanceof Array)){
                jdata = [jdata];
            }

            for(var i = 0; i < that.lines.length; i++){
                that.lines[i].last = that.accessors[i](jdata);
            }
        }
    }
    this.async_callback = this.async_callback_ctor();

    this.clear_framebuffers = function(){
        for(var i = 0; i < this.lines.length; i++){
            this.lines[i].framebuffer.splice(0, this.lines[i].framebuffer.length);
            this.lines[i].last = 0;
        }
    }
};
