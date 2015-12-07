.. _how_to_widget:

How to program a widget
=======================

You can extend the way the information is displayed in the web page by writing
custom widgets. A widget is a javascript object that is constructed by the
frontend with a layout description written by the user and sent by the
backend. Every widget is connected to some data source in order to create a
visualization of some information.

Currently, in order to paint something to the screen, the widget can only use
the *d3.js* library.

Lifetime
--------

The lifetime of a widget starts with its registration towards the frontend by
calling the function *register_widget*.

.. js:function:: register_widget(type, constructor)

   :param string type: string associated in the layout with the widget
   :param function constructor: function that returns a new widget of the given
                                type

Once the widget constructor is registered, a widget can be constructed by the
frontend when a layout with the appropriate type attribute is sent by the
backend. The frontend will pass the layout of the widget as a parameter to the
constructor.

The constructor of the widget must call (in the first lines) a SuperType
constructor with the line to inherit some common behaviour::

    Widget.call(this, layout);

The frontend will then populate the widget object with some common members
and will register it in the web page. Among this members, the frontend will 
create the svg d3js root element that the widget **must** use in order to render
something into the web page.

From now on, when an event from the backend is fired, the frontend will
notify every widget subscribed to that data source by calling the *paint*
function of the widget.

.. js:function:: paint(jdata)

   :param object jdata: JSON object with the raw data that the device is
                        sending to the frontend through the backend.

.. note::

    You should check in the paint function if the jdata is null.

The data passed to the widget's paint function is in a raw form, usually it's
complicated to manipulate this kind of information. To ease this manipulation
there exists a mechanism in lupulo called :ref:`accessors`.

Also, if the frontend needs to clear the drawings of a widget, it will call the
function *clear_framebuffers*, which is supposed to erase any drawings that the
widget is responsible for.

.. js:function:: clear_framebuffers()

   This widget's method should clear all the drawings it's responsible for, but
   it shouldn't delete anything.

Once the widget is not necessary, all the DOM information under the root svg is
going to be erased by the frontend and the JS object is going to get removed.

Aggregation
-----------

You can define a widget that uses another widgets to render some information.
This is called widget aggregation and is used heavily throughout the entire
framework. For example, :ref:`digital_clock` uses :ref:`digital_display` to
display the numbers of the time.

A widget aggregates another one when it *cooks* the layout for the new
aggregated widget and constructs it directly by typing something like::

    var new_widget = new CustomWidget(cooked_layout);

Afterwards, in the paint callback, it's going to call
*new_widget.paint(cooked_jdata)* in order to render some of the information that
the widget receives from the backend in its own paint callback.

I call to cook in this context to overwrite some of the properties of the layout
or of the jdata to fit the description and requirements of the aggregated
widget.

Some care must be taken when you decide where to put the aggregated widgets in
the DOM because, as explained earlier, the frontend expects them to be placed
under a DOM element with the id of the name of the layout that defines this
widget (layout.name). This DOM element is usually the root svg for the widget
when it doesn't aggregate more widgets, but when it does it's the responsibility
of the widget to create a new DOM element (usually a div), give it the id of the
name of the layout (layout.name), change the name of every layout used to
construct a widget (to avoid more than one DOM element to have the same id) and
finally place every widget inside that new DOM element.

When you are modifying a layout of a widget, you should always make a deepcopy
of the original layout to avoid pollution of the layout by typing::

    var layout = jQuery.extend(true, {}, layout);

as the first line of code in your source code.

You should read the source code of :ref:`digital_clock` and
:ref:`digital_display` to understand more easily how everything should work.

Css theming
-----------

All widgets should use a common css theme that can be easily customized by the
programmer of the web page through a global stylesheet that overrides the
definitions of these global css classes. In lupulo the definition of this css
classes that should define the appearance of every widget are defined in 
`main.css
<https://github.com/kudrom/lupulo/blob/master/lupulo/static/css/main.css>`_.

Dynamic sizing
--------------

As explained in the :ref:`layout`, a widget should be sized accordingly to its
size section of the layout. This size section is enforced by the frontend by
setting the width and height of the root svg element to that values.

However, when a widget has an aspect ratio, it's often a good idea to allow
partial definitions of the size in the layout file. For example, if the
programmer of the web page writes in the layout that the height of the widget
should be of 100px, the widget should complete the size by giving a width that
respects the aspect ratio and call Widget.call(layout) with that new layout.

Dynamic sizing is tricky because sometimes an svg element will not resize by
giving the svg root element a specific width or height, you will need then to
use the scale transformation. And that is quite annoying when you also have
partial definitions of the size.

You should read the source code of :ref:`digital_display` to understand more 
easily how everything should work. This widget provides partial definitions of
the size plus scale transformations to adjust its size. To see how a widget
scales without the need of a scale transformation you can see
:ref:`multiple_line`.

Responsibilities
----------------

So, to sum up, the widget must:

#. Provide a function to clear the drawings called *clear_framebuffers*.
#. Register the widget constructor with *register_factory_widgets*.
#. Call the SyperType with **Widget.call(this, layout);** inside the
   constructor in the first lines of the constructor.
#. Provide a function to clear the drawings called *clear_framebuffers*.
#. Dynamic sizing through the layout.size property.
#. Use the css theming classes.

The frontend will provide:

#. A root svg element in *this.svg* that the widget must use to write something
   into the web page with d3.js.
#. A notification whenever some data arrives that the widget is subscribed to
   through the *paint* callback.
#. The accessors mechanism.
#. Widget aggregation.

Utils
-----

There are a bunch of utils which you might need to use when you are programming
your own widget. All of these functions are in utils.js, so check that out for
more information.

.. js:function:: get_complete_event_name(event_name)

    This function returns a string with the complete name of an event source
    defined in the data schema definition. The complete name is made of the id
    of the device and the event source of the stream.

    This function is the inverse of *get_event_name*

    :param string event_name: name of the event source as it is written in the
                              data schema definition

.. js:function:: get_event_name(source_event)

    This function returns a string with the event source name of a complete
    event source name, which is the name of an event source as it appears in the
    data schema definition.

    This function is the inverse of *get_complete_event_name*

    :param string source_event: complete name of an event source.

.. js:function:: pretty(obj, spaces_n, print_indexes)

    Recursive function that returns a string with a pretty representation of the
    object given as an argument.

    :param Object obj: object to pretty print.
    :param int spaces_n: internal parameter, you **must** call it with the 0
                         value.
    :param boolean print_indexes: whether to print the indexes of a list or not.

.. js:function:: validate_requirements(requirements, layout)

    Function to validate the requirements that a widget demands of a layout
    given by the user.

    :param List requirements: List containing all the keys that the layout must
                              provide.
    :param Object layout: Layout definition of the widget.

.. js:function:: add_alert(type, text)

    This function will render at the top of the web page a box displaying the
    text you pass to it as an argument.

    :param enum type: string describing the level of relevance of the text,
                      it can be success, info, warning and danger.
    :param string text: text to display in the box.
