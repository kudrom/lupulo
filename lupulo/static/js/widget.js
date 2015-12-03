function fill_widget_prototype(constructor){
    // This function is called back every 1s to render the animation of every
    // line in the graph
    constructor.prototype.tick = function(widget) {
        // Call the callback to paint the widget
        widget.paint(widget.jdata);

        // BUG #2079, registers the callback through d3js to avoid
        // funky slide movements
        widget.tick_anchor.transition()
          .duration(1000)
          .each("end", function(){widget.tick(widget)});

    }

    // Constructor of the async callback used to provide this/that to
    // the async callback
    constructor.prototype.async_callback_ctor = function() {
        var widget = this;
        return function(event){
            var jdata = JSON.parse(event.data);
            if(widget.jdata === null){
                widget.jdata = {};
            }
            widget.jdata[event.type] = jdata;
        }
    }
}

Widget = function(layout){
    // JSON data for the paint function
    this.jdata = null;

    // Event sources the widget is subscribed to
    this.event_sources = [];

    // The margin is optional
    if('margin' in layout){
        margin = layout.margin;
    }else{
        margin = {top: 0, right: 0, bottom: 0, left: 0};
    }

    // Sizes of the canvas
    this.width = layout.size.width - margin.left - margin.right;
    this.height = layout.size.height - margin.top - margin.bottom;

    // Setup the svg root element
    this.svg = d3.select(layout.anchor).append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom);
    this.svg.attr('id', layout.name);

    if('viewBox' in layout){
        this.svg.attr('viewBox', layout.viewBox);
    }

    this.svg = this.svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    // Anchor for the transition in the tick function
    this.tick_anchor = this.svg.append("g").attr("class", "tick_anchor");

    // Asynchronous mechanism
    this.async_callback = this.async_callback_ctor();
}
