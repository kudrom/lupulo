.. _battery:

Battery
=======

The battery widget will render a digital display of the level of battery of a
device plus a dynamic drawing of a battery as in the following two images:

.. image:: images/battery.png

.. image:: images/battery_empty.png

The battery provides dynamic sizing and doesn't define any requirement, it's
normal size is 570x350 pixels.

example
-------

The following is a correct layout for the Battery widget::

    {
        "battery": {
            "type": "battery",
            "size": {
                "height": 100
            },
            "margin": {
                "top": 0,
                "bottom": 0,
                "left": 0,
                "right": 0
            },
            "event_names": ["battery"],
            "anchor": "#battery-anchor",
            "accessors": [{
                "type": "primitive"
            }]
        },
    }
