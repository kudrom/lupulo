Line = function(name){
    this.name = name;
    // Last value read by the async callback
    this.last = 0;
    // Array for the data displayed
    this.framebuffer = [];
    // SVG path
    this.path;
    this.line;
}

MultipleLine = function(range, seconds, lines){
    // Width of the time scale
    this.seconds = seconds;
    this.lines = [];
    for(var i = 0; i < lines.length; i++){
        this.lines.push(new Line(lines[i]));
    }

    var margin = {top: 20, right: 20, bottom: 20, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain([0, this.seconds - 1])
        .range([0, width]);
    this.x = x;

    var y = d3.scale.linear()
        .domain(range)
        .range([height, 0]);
    this.y = y;

    var color = d3.scale.category10()
        .domain(lines);

    for(i = 0; i < lines.length; i++){
        this.lines[i].line = d3.svg.line()
            .x(function(d, ii) { return x(ii - 1); })
            .y(function(d, ii) { return y(d); });
    }

    var svg = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.svg.axis().scale(x).orient("bottom"));

    svg.append("g")
        .attr("class", "y axis")
        .call(d3.svg.axis().scale(y).orient("left"));

    this.container = svg.append("g")
        .attr("class", "container");

    for(i = 0; i < lines.length; i++){
        this.lines[i].path = this.container.append("g")
            .attr("clip-path", "url(#clip)")
          .append("path")
            .datum(this.lines[i].framebuffer)
            .attr("class", "line")
            .attr("stroke", function(d){return color(lines[i])})
            .attr("d", this.lines[i].line);
    }

    this.tick = function(that) {
        for(var i = 0; i < that.lines.length; i++){
            // push a new data point onto the front
            that.lines[i].framebuffer.unshift(that.lines[i].last);

            // redraw the line, and slide it to the right
            that.lines[i].path
              .attr("d", that.lines[i].line)
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

    this.async_callback = function() {
        var that = this;
        this.tick(this);
        return function(event){
            var jdata = JSON.parse(event.data);
            if(!(jdata instanceof Array)){
                jdata = [jdata];
            }

            for(var i = 0; i < that.lines.length; i++){
                that.lines[i].last = jdata[i];
            }
        }
    }
};
