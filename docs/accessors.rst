.. _accessors:

Accessors
=========

Suppose you are building a widget to visualize the historical data of some of
the sensors of your robot. As explained in :ref:`how_to_widget`, you receive
the raw data in the *paint* function. That raw data follows the data schema the
device is transmitting the information with. So, to access the information in
the widget, you have to know what schema the device is following, right? Well,
hell no. That's what you use the accessors for.

An accessor is a function that returns datums that the widget is expecting to
work with. The widget doesn't know how is the structure of the raw data it's
receiving. It just needs to render a number, a date or a list (a datum). But
that number, date or list can be buried in some aggregate structure into the
raw data. The accessor is therefore responsible to return some datum from some
complex aggregated raw data that is defined in the data schema file.

An accessor is described in the layout file of a web page. It's built by the
widget, usually in its constructor, and when data arrives to the widget, it's
invoked by the paint function with the raw data as an argument. As described
earlier, the accessor then returns some data inside the raw data that the widget
wants to render.

Mechanism
---------

The widget should not be dependent on the data schema. If you change the data
schema, you shouldn't change the code inside a widget. Otherwise, you couldn't
use easily a widget for several devices with different data schemas.

But a widget has to render the data the device is sending. And that data follows
the data schema of the device. So apparently, the widget must know the data
schema in order to access the raw data in the paint function. And that's a
problem of extensibility because if the data schema changes, the code inside the
widget must change too.

The solution is to provide a mechanism to allow a widget to extract datums from
the raw data without knowing directly the data schema definition.

Remember from previous sections that the web page is made of widgets constructed
with a definition called layout. Each widget subscribes to different event 
sources, and each event source is defined by some section in the data schema.

In the layout of the widget, there is a section called accessors, which
describes the data schema definition of the event source to the widget through
the accessors mechanism.

When the widget is constructed, the frontend passes it the entire layout.
Afterwards, if the widget uses accessors, the widget calls the *get_accessors*
function with the accessors section in the layout definition. This function
returns a list of accessors functions for every datum the widget is interested
in.

When a widget calls one of this accessors with some raw data from an event
source, the accessor already knows the structure of the event source and returns
the datum the widget is interested in.

This way, the widget don't access the data schema: the accessors do this for
him. But the widget must construct, store and call them explicitly. That's why
the accessors are optional.

This is how the accessors work, for some explanation of the layout format and
the way a widget should use them, see the following sections.

Layout description
------------------

To describe the accessors that the widget will use, you first must provide a
section in the layout for the widget called *accessors* which can be a list or
an object that the *get_accessors* function will read to return the list of
accessor functions.

If the *accessors* section is a list, the *get_accessors* function will return a
list with all the accessors defined in the section. If it's an object, the
*get_accessors* function will return an object indexed in the same way the
definition is.

You can use several kinds of accessors for the same widget, and you can chain
them to access data in a complicated schema. Every accessor has some custom
arguments, but some of them are shared.

Also, an accessor description in the layout can be a generator of accessors.
This way you can summarize repetitive information in a single definition that
generates several accessors. See :ref:`index` for an example.

All accessors must have an obligatory attribute called *type* which defines the
type of the accessor. This type can be one of the built-in accessors or one
of your own accessors.

Every accessor is first tied to an *event* source with the event argument. The
accessor will only get information from the event source it's tied to. If no
*event* argument is provided, the frontend will tie the accessor to the first
event source present in the *event_names* property of the layout. If the *event*
of the accessor is not present on the *event_names*, the accessor is rejected
when it's being constructed in the frontend, so pay attention to the browser's
console if something weird is happening.

Built-in accessors
------------------

Once you know that an accessor is described in the layout and some of its
arguments, it's time now to present you the built-in accessors present in every
installation of lupulo with its required arguments, which you must add to the
layout file of the desired widget layout.

primitive
#########

This is the easiest accessor, it returns the data directly associated to the
event source and have no arguments.

For example, if I had the following data schema::

    {
        "battery": {
            "type": "number",
            "range": [0, 100]
        }
    }

And the following layaout::

    {
        "battery_widget":{
            "type": "multiple_line",
            "event_names": ["battery"],
            "anchor": "#battery",
            "name_lines": ["Battery"],
            "y_name": "%",
            "accessors": [{
                "type": "primitive"
            }]
        }
    }

Because the accessors section is a list, the *MultipleLine* widget will access
the accessors as a list (in this case with one primitive accessor). For example:

.. code-block:: javascript

    var accessors = get_accessors(layout.accessors);
    for(var i = 0; i < accessors.length; i++){
        var accessor = accessors[i];
    }

If the accessors section were an object instead, the *MultipleLine* widget would
access the accessors as an object. For example::

    {
        "battery_widget":{
            "type": "multiple_line",
            "event_names": ["battery"],
            "anchor": "#battery",
            "name_lines": ["Battery"],
            "y_name": "%",
            "accessors": {
                "battery_accessor":{
                    "type": "primitive"
                }
            }
        }
    }

.. code-block:: javascript

    var accessors = get_accessors(layout.accessors);
    var accessor = accessors.battery_accessor

The widget defines how it wants to receive the accessors: as a list or as an
object. Therefore, every layout description of the widget must stick to this
preference and write the accessors section with all of this in mind.

.. _index:

index
#####

This accessor returns a **list of accessors**. Each of this returned accessors
extract data from a list event source in a custom position. As a whole, the
entire sequence of accessors returned by this accessor extract a slice of data
from the event source. This slice of data accessed by the list of accessors
returned by this accessor is defined by its two arguments:

start
+++++

The starting index of the slice of data.

end
+++

The ending index of the slice of data.

So, for example, if I had a data schema like this::

    {
        "batteries": {
            "type": "list",
            "length": 3,
            "item_type": "enum",
            "item_range": [0, 100]
        }
    }

And a layout like this::

    {
        "batteries_widget": {
            "type": "multiple_line",
            "event_names": ["batteries"],
            "anchor": "#batteries",
            "name_lines": ["Second-battery", "Third-battery"],
            "y_name": "%",
            "accessors": [{
                "type": "index",
                "event": "batteries",
                "start": 1,
                "end": 3
            }]
        }
    }

The widget *batteries_widget* will display the state of the two last batteries
of the widget's subscribed data source.

dict
####

This accessor returns an accessor that extracts some data in a dict structure by
a given key, which is its unique argument.

key
+++

The key of the raw data that the accessor should look up when returning some
data.

So, for example, if I had the following schema::

    {
        "batteries": {
            "type": "dict",
            "keys": ["state", "charge"],
            "state_type": "enum",
            "state_values": ["on", "off"],
            "charge_type": "number",
            "charge_range": [0, 100]
        }
    }

And a layout like this::

    {
        "batteries_widget": {
            "type": "multiple_line",
            "event_names": ["batteries"],
            "anchor": "#batteries",
            "name_lines": ["Battery"],
            "y_name": "%",
            "accessors": [{
                "type": "dict",
                "event": "batteries",
                "key": "charge"
            }]
        }
    }

The widget *batteries_widget* will render the charge of the battery.

Chaining
--------

As you should know, the data schema language provides recursive definitions so
you can define complex structures like list of dictionaries. Chaining is the
mechanism the accessors follow to extract information from this complex
structures.

You define chaining in an accessor with the *after* property in the layout
section for the accessors definition. This property is the description of
a **list** of accessors (not an object) that will extract information from the
already extracted information of its parent when the accessor is called.

.. warning::

    You cannot use an object describing an accessor in the after section of a
    description of an accessor. You only can use a list.

For example, if you had this schema::

    {
        "motor": {
            "type": "list",
            "length": 2,
            "item_type": "dict",
            "item_keys": ["speed", "turn_radius"],
            "item_speed_type": "number",
            "item_speed_range": [0, 5],
            "item_turn_radius_type": "number",
            "item_turn_radius_range": [0, 3]
        }
    }

And a layout like this::

    {
        "motor": {
            "abstract": true,
            "parent": "global",
            "event_names": ["motor"],
            "anchor": "#motors"
        },
        "speed": {
            "parent": "motor",
            "name_lines": ["speed-left", "speed-right"],
            "y_name": "Speed",
            "accessors": [{
                "type": "index",
                "start": 0,
                "end": 2,
                "after": [{
                    "type": "dict",
                    "key": "speed"
                }]
            }],
            "range": [0, 5]
        }
    }

There will be two accessors, one to extract the speed of the left and right
wheel respectively.

Usage
-----

To use the accessors, the programmer of the layout file should write accessors
sections for the widget's layouts as described in the previous paragraphs
attending to the requirements the widget places on the accessors.

Of course, the programmer of the widget should use that description to extract
information from the raw data. To use them in your widget, you must first
construct them by calling the function *get_accessors*:

.. js:function:: get_accessors(description)

   :param object description: JSON object part of the layout describing the
                              accessors
   :returns: list or object of accessors generated from the description

As explained above, the widget must fix if it wants to receive the accessor as a
list or as an object indexed by some fixed keys. The user of the widget then
must stick to this definition.

Once the widget has the list of accessors, it should store them as a private
member and use them when new data arrives in the paint method. You just have to
get one of the accessors and call it with the raw data received by the widget as
its unique parameter. The accessor will return all the data that the widget is
interested in.

Building an accessor
--------------------

Finally, if you want to extend the number of accessors that exist, you can
register your own kind of accessor with the function *register_accessor*

.. js:function:: register_accessor(type, accesor)

   :param string type: String used to link an accessor to its description in the
                       layout file
   :param function accessor: The constructor of the accessor.

As you can see, you register a constructor of an accessor that must return a
list of accessors. This constructor receives a JSON description of the accessors
in the layout file for the corresponding widget and returns the accessor
function.

.. warning::

    Every accessor constructor must return a list of accessors.

The accessor function will be called by the widget when some data arrives and it
will return the data described in the accessors section of the layout.

For example, this is the registration for the primitive accessor:

.. code-block:: javascript

    register_accessor("primitive", function(description){
        var event_source = description.event;

        return [function(jdata){
            var event_name = get_complete_event_name(event_source);
            if(!(event_name in jdata)){
                console.log("[!] " + event_name +
                            " is not an event source of data.");
                return 0;
            }

            return jdata[event_name];
        }];
    });

As you can see, the constructor returns a function that gets the complete event
name that the widget is subscribed to through the accessors section in its
layout file and then returns the primitive data associated with that
*event_name* whenever it can.
