.. _led:

Led
===

The led widget will render in a colorful way information related to some
primitive value according to the mapping given in the layout as seen in the
following image:

.. image:: images/led.png

The led widget provides dynamic sizing and two parameters. The led will be
placed at the center of the rectangle defined by layout.size, if that rectangle
is not a square and the radius is not big enough, the led will be cropped.

radius
------

The radius in pixels of the led.

mapping
-------

Dictionary that allows you to specify what color to render given some value.
There exists two main possibilities depending if the value to render is a number
or a enumeration.

If the value is a number you will have to provide a key with the text "\* to \*"
where the \* is a number. For example, for a numerical event source of range
[0, 100] you could write the following mapping::
    {
        "mapping": {
            "0 to 10": "red",
            "10 to 50": "rgb(255, 186, 12)",
            "50 to 90": "#FFBA0C",
            "90 to 100": "green"
        }
    }

If the value is a enumeration you will have to write in each key a value of the
given enumeration. For example, for a enum event source with the values 'on',
'off' and 'null', you could write the following mapping::
    {
        "mapping": {
            "on": "green",
            "off": "red",
            "null": "grey"
        }
    }

example
-------

The following is a correct layout for the Led widget::

    {
        "led-control": {
            "type": "led",
            "size": {
                "height": 100
            },
            "event_names": ["led"],
            "anchor": "#battery-anchor",
            "accessors": [{
                "type": "index",
                "start": 0,
                "end": 1
            }],
            "radius": 40,
            "mapping":{
                "on": "green",
                "off": "red",
                "null": "grey"
            }
        },
    }
