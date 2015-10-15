Data schema language
====================

As said in the :ref:`overview`, the data schema language is a JSON file that
describes the schema that the data sent by the device follows.

The data schema basically serves two main goals:

#. Description of the number of data sources that the device provides.
#. Description of the data sent in every data source.

A data source is a stream of data provided by the device to the frontend. It's
**usually** paired with the concept of sensor. In this way, the data measured
by one sensor is usually packaged into one data source that the widgets can
listen to. The user of the framework must decide how many data sources {s}he
wants to provide.

The framework will provide events that the widgets can listen to in order to get
updates for a concrete data source. Each widget in the frontend will listen to
one or more data sources from the device and will construct the visualizations
with all of that information.

Once the device sends some data through a data source, every widget that is
listening to that data source will be notified.

Each data source is described by a JSON object (in the data schema file) filled 
with some key-value pairs that describe the properties of the data associated
with a data source. There is only one obligatory property of every data source:
its *type*.

The type of a data source determines how the data is going to be verified by the
backend when it is going to be forwarded to the frontend. Each type defines its
own properties that every data source description of that type must stick to.

Currently there are two kind of types:

#. Primitive types
#. Aggregated types

The aggregated types are a composition of primitive types.

From now on, all data sources types will be described. To see an example of a
correct data schema file, go to *tests/data_schemas/complete.json* in the
project directory.

number
------

Primitive data source type associated with a decimal number. It defines only the
range argument, which is a list of two elements that defines the minimum and
maximum value that the data of the associated data source must stick to. That
way, if we'd like to provide a data source for a battery, we could write it this
way:::

    "battery": {
        "type": "number",
        "range": [0, 100]
    }

date
----

Primitive data source type associated with a epoch time. It defines no arguments.::

    "date": {
        "type": "date"
    }

enum
----

Primitive data source type associated with an enumerated value. It defines 
one attribute called values that is a list with all the allowed values of the
enumeration. For example, if we'd like to describe a led state we could write::

    "led": {
        "type": enum,
        "values": ["on", "off"]
    }

list
----

Aggregated data source type which is a sequence of other data source types. It
defines two different kinds of attributes.

The first is a simple one called length that sets the length of the sequence.

The second kind of attributes start with the item\_ preffix. These set of
attributes defines the attributes of every data in the sequence. There are as
much attributes as necessary to fully define the data source type of the data
enclosed in the sequence.

For example, if we'd like to define a list of 8 leds, we could write::

    "leds": {
        "type": "list",
        "length": 8,
        "item_type": "enum",
        "item_values": ["on", "off"]
    }

If we'd like to define a list of 3 batteries, we could write::

    "batteries": {
        "type": "list",
        "length": 3,
        "item_type": "number",
        "item_range": [0, 100]
    }
    
Notice how in the first definition we need *item_values* and in the second
definition we need *item_range* to fully define the aggregated data source.

dict
----

Aggregated data source type which is a key/value pair of other data sources.
Like the list data source type, it defines two different kind of attributes.

The first one is a simple one called keys with is a list of the keys in the
dictionary.

The second kind of attributes start with every key of the dictionary followed by
an underscore. These attributes must fully define the data source associated
with the given key.

For example, if we'd like to define some leds by its state and intensity, we
could write::

    "leds": {
        "type": "dict",
        "keys": ["state", "intensity"],
        "state_type": "enum",
        "state_values": ["on", "off"],
        "intensity_type": "number",
        "intensity_range": [0, 4]
    }

All of this data sources can be nested in complex data schemas, for example if
we'd like to describe two motors by its speed and turn radius, we could write::

    "motors": {
        "type": "list",
        "length": 2,
        "item_type": "dict",
        "item_keys": ["speed", "turn_radius"],
        "item_speed_type": "number",
        "item_speed_range": [0, 5],
        "item_turn_radius_type": "number",
        "item_turn_radius_range": [0, 3]
    }
