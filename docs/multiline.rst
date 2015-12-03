.. _multiple_line:

MultipleLine
------------

MultipleLine is a widget that displays numeric information in a line graph with
multiple lines as can be seen in the image:

.. image:: images/multiline.png

MultipleLine uses the accessors mechanism, so you should provide an accessor
section in your layout that describes how the widget can fetch the data from
your data schema. This accessors section must be a list.

The obligatory attributes for the layout are:

name_lines
::::::::::

List containing the names of the lines rendered by the widget. This list is used
to know how many lines are going to be rendered and for the legend of the graph.

y_name
::::::

String for the name that will be displayed in the y axis of the graph.

seconds
:::::::

Length of the time axis.

range
:::::

Domain of the data.

example
:::::::

The following is a correct layout for the MultipleLine widget::

    {
        "global": {
            "abstract": true,
            "type": "multiple_line",
            "size": {
                "width": 760,
                "height": 500
            },
            "margin": {
                "top": 0,
                "bottom": 0,
                "left": 0,
                "right": 0
            },
            "seconds": 100
        },

        "battery": {
            "parent": "global",
            "event_names": ["battery"],
            "anchor": "#battery-anchor",
            "name_lines": ["Battery"],
            "y_name": "Battery",
            "accessors": [{
                "type": "index",
                "start": 0,
                "end": 1
            }],
            "range": [0, 100]
        },
    }
