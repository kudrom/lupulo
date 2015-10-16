.. _accessors:

Accessors
=========

An accessor is an object which consists of a name and some parameters if
necessary. The name references a JS function that should return a function that
will be called when an event of a event source of the described widget is
called in the frontend. The 

For example, if there is an event source made of the data of 8 leds and the 
widget only wants to render the state of the first 4, I could do this:::

    {
        "first_four_leds": {
            "event_name": "leds",
            "accessors": [
                {
                    "name": "index",
                    "start": 0,
                    "end": 4
                }
            ]
        }
    }
