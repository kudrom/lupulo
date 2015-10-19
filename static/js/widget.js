Widget = function(){
    // jdata is the parsed data received from the sse connection
    this.jdata = null;

    // This function is called back every 1s to render the animation of every
    // line in the graph
    this.tick = function(widget) {
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
    this.async_callback_ctor = function() {
        var widget = this;
        return function(event){
            var jdata = JSON.parse(event.data);
            if(!(jdata instanceof Array)){
                jdata = [jdata];
            }

            widget.jdata = {event.type: jdata};
        }
    }
}
