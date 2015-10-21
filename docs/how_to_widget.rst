.. _how_to_widget:

How to program a widget
=======================

You can extend the way m3pdi_ui renders the web page by writing custom widgets.
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
there exists a mechanism in m3dpi_ui called :ref:`accessors`.

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
