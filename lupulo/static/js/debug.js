(function (){
    function print(event){
        return function(data){
            $('#'+event).text(event + ': ' + data.data);
        }
    }
    var pipe = new EventSource("/subscribe"),
        id = 1,
        events = ["housekeeping", "date", "battery", "distances", "rotation", "direction", "acceleration", "motors", "floor"],
        father = $('.information');

    for(var i = 0; i < events.length; i++){
        var event = events[i],
            event_source = 'id' + id + '-' + event;
        father.append('<div id="' + event + '"></div>');

        pipe.addEventListener(event_source, print(event))
    }
})();
