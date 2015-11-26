.. _how_to_widget:

How to program a widget
=======================

You can extend the way lupulo renders the web page by writing custom widgets.
A widget is a javascript object that is constructed by the frontend with a
layout description written by the user and serviced by the backend. Every widget
is connected to some data source in order to create a visualization of some
information measured by a device.

Currently, in order to paint something to the screen, the widget can only use
the *d3.js* library.

The lifetime of a widget starts with its registration towards the frontend by
calling the function *register_widget*.

.. js:function:: register_widget(type, constructor)

   :param string type: string associated in the layout with the widget
   :param function constructor: function that returns a new widget of the given
                                type

Once the widget constructor is registered, a widget is constructed by the
frontend when a layout with the appropriate type attribute is sent by the
backend. The frontend will pass the layout of the widget as a parameter to the
constructor.

The constructor of the widget must call (in the first lines) a SuperType
function that populates the widget with some members necessary for the frontend
Among this members, the frontend will create the svg root element that the
widget **must** use in order to render something in the web page.

Once the constructor function returns a widget, the frontend
populates some attributes of the widget and registers it in the web page.

From now on, when an event from the backend is fired, the frontend will
notify every widget subscribed to that data source by calling the *paint*
function of the widget.

.. js:function:: paint(jdata)

   :param object jdata: JSON object with the raw data that the device is
                             sending to the frontend through the backend.

The data passed to the widget's paint function is in a raw form, usually it's
complicated to manipulate this kind of information. To ease this manipulation
there exists a mechanism in lupulo called :ref:`accessors`.

Also, if the frontend needs to clear the drawings of a widget, it will call the
function *clear_framebuffers*, which is supposed to erase any drawings that the
widget is responsible for.

.. js:function:: clear_framebuffers()

   This widget's method should clear all the drawings it's responsible for.

So, to sum up, the widget must:

#. Provide a function to clear the drawings called *clear_framebuffers*.

#. Register the widget constructor with *register_factory_widgets*.
#. Call the SyperType with **Widget.call(this, layout);** inside the
   constructor.
#. Provide a function to clear the drawings called *clear_framebuffers*.

The frontend will provide:

#. A root svg element in *this.svg* that the widget must use to write something
   into the web page with d3.js.
#. A notification whenever some data arrives that the widget is subscribed to
   through the *paint* callback.
#. The accessors mechanism.

Finally, a widget should display in the web pages all kinds of information
relevant to the user with the alerts library. You can use the function
*add_alert* defined here:

.. js:function:: add_alert(type, text)

    This function will render at the top of the web page a box displaying the
    text you pass to it as an argument.

    :param enum type: string describing the level of relevance of the text,
                      it can be success, info, warning and danger.
    :param string text: text to display in the box.

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
