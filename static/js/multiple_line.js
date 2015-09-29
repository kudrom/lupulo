MultipleLine = function(){
    var seconds = 100,
        data = [];

    var margin = {top: 20, right: 20, bottom: 20, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .domain([0, seconds - 1])
        .range([0, width]);

    var y = d3.scale.linear()
        .domain([0, 100])
        .range([height, 0]);

    var line = d3.svg.line()
        .x(function(d, i) { return x(i); })
        .y(function(d, i) { return y(d); });

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

    var path = svg.append("g")
        .attr("clip-path", "url(#clip)")
      .append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

    this.tick = function(that) {

      // push a new data point onto the front
      if (that.buffer.length != 0){
          that.last = that.buffer.pop();
      }
      that.data.unshift(that.last);

      // redraw the line, and slide it to the right
      that.path
          .attr("d", that.line)
          .attr("transform", null)
        .transition()
          .duration(1000)
          .ease("linear")
          .attr("transform", "translate(" + that.x(1) + ",0)")
          .each("end", function(){that.tick(that)});

      // pop the old data point off the back
      if(that.data.length == that.n + 1){
          that.data.pop();
      }
    }

    this.wrapper = function() {
        var that = this;
        return function(event){
            var jdata = JSON.parse(event.data);
            that.buffer.push(jdata);
        }
    }

    this.line = line;
    this.path = path;
    this.x = x;
    this.data = data;
    this.last = 50;
    this.buffer = [];
};
