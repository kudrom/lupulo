.. _layout:

Layout language
===============

As said before throughout the documentation, one of the core concepts in
lupulo are the layouts the user writes to define the web page.

A layout is an object that the frontend passes to a widget when it's going to be
constructed. The main responsibility of a layout is to let the widget know what
and how to render the information that the device is sending him. Also a layout
provides a description to define what widgets to construct or where they should
be placed into the web page.

The *layout file* is a JSON file which lists all the layouts that are needed to
render a web page. A layout is filled with data that:

#. The backend and frontend need to construct the appropriate widget for a given
   layout.
#. The widget needs itself to render the information.

Every layout thus shares some common attributes that they must provide in order
to be valid lupulo layouts. But depending on the type of widget that the
layout is describing, another set of attributes are needed. These last
attributes are defined by the widget.

An important note is that if a layout doesn't have all the obligatory attributes
that the framework needs, you will be notified when you launch the server. But
if the layout doesn't have all the obligatory attributes that the widget needs,
you will be notified in the web page alerts.

The raw layout file is compiled before sending it to the frontend. The compile
process is focused on solving the inheritance tree of the layout file and 
convert it to a list of layouts without parents.

There are several attributes defined in the backend that will be described
shortly. Every layout is indexed by a name that is used inside the layout file.
This name is also added to the compiled layout that is sent to the frontend in
the *name* attribute.

One key attribute is the *event_names* attribute, that describes the data
sources the widget is listening to. It is a list containing the names of the
data sources the widget is listening to. Take a look at
:ref:`data-schema-language` if you don't know what I'm talking about.

Another very important attribute is the type attribute, that defines which type
of widget will be defined by the layout.

Other obligatory attribute is *size* which is a dictionary with two keys:
*height* and *width*. The size defines, as his name implies, the size of the
widget in the web page.

In order to add the widget to the web page, the web page needs to have a html
element to bind the widget to. This element is called the *anchor* of the widget
in the web page and is another obligatory attribute of every layout in the
layout file. This anchor can be any selector of jquery that resolves to an html
element.

Inheritance
-----------

Due to the verbosity and duplicity of the attributes of a layout, the layout
language provides a way to inherit attributes from a parent. Every attribute
defined in a parent that isn't defined in a child will be inherited in the
child. If an attribute exists both in the child and parent, the child value for
the attribute overwrites that of the parent in the child definition.

There are two kinds of layouts:

#. **Leaf layout**: a layout that will be sent to the frontend to construct a
   widget.
#. **Abstract layout**: a layout that won't be sent to the frontend but that can
   be used inside the layout file.

A parent must be abstract in order to be considered for inheritance.

So, a leaf layout will be sent to the frontend to construct a given widget
that is described by the direct attributes of his layout and that ones of his
parent. However, the abstract layout won't be sent to the frontend so no widget
will be constructed with the possibly partial attributes of the parent layout.

To describe that a layout is abstract, you must add the abstract boolean
attribute to the layout with a value of *true*.

To describe that a layout inherits from another one, you must add the parent
string attribute to the layout with the value of the name attribute of the
parent.

It isn't allowed multiple inheritance but severals levels of inheritance are
possible.

For example, if the layout battery would inherit from the global layout, a
possible layout file could be::

    {
        "global": {
            "abstract": true,
            "size": {
                "width": 960,
                "height": 500
            },
            "type": "multiple_line"
        },

        "battery": {
            "parent": "global",
            "event_names": ["battery"],
            "type": "circular_meter"
        }
    }

In this example, battery will be sent to the frontend with the compiled
layout::

    [
        {
            "name": "battery",
            "size": {
                "width": 960,
                "height": 500
            },
            "event_names": ["battery"],
            "type": "circular_meter"
        }
    ]

Accessors
---------

Usually a widget can only subscribe to an entire data source even when it only
needs some information of the entire event stream. To access only to some
information of an entire event stream, the widget should use the
:ref:`accessors` mechanism.

Widgets
-------

There are several widgets provided by default in the base distribution of
lupulo.

As said above, each widget can define infinite attributes that the layout must
provide in order to be constructed and added to the web page.

The widgets distributed currently in lupulo are:

.. toctree::
    :maxdepth: 1

    multiline.rst
