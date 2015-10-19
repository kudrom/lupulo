How to program a widget
=======================

You can extend the way m3pdi_ui renders the web page by writing custom widgets.
A widget is a javascript object that is constructed by the frontend with a
layout description written by the user and serviced by the backend. Every widget
is connected to some data source in order to create a visualization of some
information measured by a device.

Currently, in order to paint something to the screen, the widget can only use
the *d3.js* library. Furthermore, the widget must make public the root svg
element of the entire drawing with a property of that name.

The lifetime of a widget starts with its registration towards the frontend by
calling the function *register_factory_widgets*.

Once the widget constructor is registered, a widget is constructed by the
frontend when a layout with the appropriate type attribute is sent by the
backend. The frontend will pass the layout of the widget as a parameter to the
constructor. Once the constructor function returns a widget, the frontend
populates some attributes of the widget and registers it in the web page.

From now on, when an event from the backend is fired, the frontend will
notify every widget subscribed to that data source by calling the *paint*
function of the widget.

Also, if the frontend needs to clear the drawings of a widget, it will call the
function *clear_framebuffers*, which is supposed to erase any drawings that the
widget is responsible for.

So, to sum up, the widget must:

#. Register the widget constructor with *register_factory_widgets*.
#. Make public the root svg element of the drawings as an attribute of the
   widget object.
#. Provide a function to clear the drawings called *clear_framebuffers*.

This way, the widget will be notified with some data in the *paint* callback by
the frontend when there is data available for the event sources the widget is
subscribed to.
