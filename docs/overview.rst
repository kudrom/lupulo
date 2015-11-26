.. _overview:

Overview
========

To develop a device which interacts with its environment, it's usually needed a
visualization of the sensory data in order to understand the behaviour of the
device in the development stages.

Once a prototype of the device has been built, it's usually also needed a rich 
user interface to command it and also to track its progress in a more realistic
deployment.

lupulo is a framework that allows you to build several web-based user
interfaces that will allow you to understand much better the device you are
building with some visualization of the sensory information and also to build
rich user interfaces to command it with all the relevant information at sight.

You just need to understand how the data is going to be sent from your device
and how you want to visualize it at a web page. For the rest, lupulo will take
care.

Description
-----------

lupulo is a framework built in python and javascript to build visualizations
of data sent by devices that measure its surroundings, typically robots or IoT
devices. It can be used to monitor the state of the device and command it in
real time or to record a session and analyze the data afterwards.

Its main use cases range from prototypical design where it's useful to see the
raw data that the device is measuring from its environment to a control panel to
command the device once it's deployed in the production environment.

Different user interfaces serving different needs for the same device can be
built very quickly. That way if the data schema or the visualization needs of
the information change during development, it's quite straightforward to replace
the current visualization with one that answers to the new changes.

Several devices can be monitored by the same user interface at the same time as
long as all of them follow the same data schema for the information they are
sending.

With the base installation there are a bunch of *widgets* which can be used from
the beginning to build your web page. Of course, you can also write your own
*widgets* if you need to visualize information in a specific way and plug them
into the framework very easily.

You can also build new data connections to connect your device with the outside
world and plug them into lupulo. This way, you can use the default
configurations of the framework and use it as a quick user interface to
understand better your device or you can personalize it to build a rich user
interface.

lupulo has been built to run in a RaspberryPi, but another hardware
configurations are possible as long as GNU/Linux is used to run the backend.

How it works
------------

lupulo is composed of two main components:

* **The backend** which makes the connection with the device, receives the data
  sent by the device, records it and sends it back in real time to the frontend.
* **The frontend** which renders the information received by the backend in real
  time in several *widgets* chosen by the programmer of the final web page.

lupulo is configured in *settings.py*, where you establish the data link
between the device and the backend, the host that is going to store the
information, the *data schema* that all the information received by the backend
is following, a description of the web page which we call *layout* and several
other parameters.

What you must provide to build up the final web page is a description of the
*data schema* and a *layout* that defines the final web page.

Both of these documents are json files with a specific format defined in another
sections of this documentation.

The *data schema* is made of descriptors that describe an important source event
in the device. For example, you can have a descriptor for the speed of a robot
and another one for its direction.

The *layout* is made of descriptors that bind a source event defined in the data
schema to a widget in the user interface. For example, for the speed of the
robot you can have two widgets, a line graph that shows the speed of the robot
in the last 90 seconds and a speedometer that displays in a graphical way the
current speed of the robot.

As said above, you can expand both the types of data descriptors to recognize
different data formats and also different widgets to display information in the
web page in different ways.

There are more mechanisms to customize your web page that will be discussed in
the following sections of this documentation.

Installation
------------

*lupulo* is a python2 package uploaded to `pip 
<https://pypi.python.org/pypi/lupulo/>`_, so to install it you can type in a
linux console::

    pip install lupulo

Currently only python2 is supported so you need a proper installation of python
in order to install it.

You also need to have a proper installation of mongodb if you want to register
the information gathered by the backend from the device with mongodb.

Use
---

In order to launch the lupulo's server, first you have to have create a folder
structure for a valid lupulo's project. To do that, you must execute from the
project's folder the program **lupulo_create**. This will create a folder
structure similar to this one::

    <project folder>
    `---templates/
    `---static/
    `---data_schema.json
    `---layout.json
    `---settings.py
    `---urls.py

The templates and static directories and the urls.py file are discussed in 
:ref:`templates`.

The data_schema json file is discussed in :ref:`data-schema-language`.

The layout json file is discussed in :ref:`layout`.

Finally, the settings file is discussed in :ref:`settings`.

Then you must launch the lupulo server with the command **lupulo_start**. You
can start lupulo in the background if you add the *--daemonize* option to the
*lupulo_start* program.

.. warning::

    For the moment, you need superuser permissions to execute some listeners.

.. note::

   See the settings before running the server.

.. _debugging:

Debugging
---------

lupulo also provides some utilities to debug the web page.

The first one is a sse client that will allow you to listen to the information
that the backend is sending to your web page. The sse client will create a sse
connection towards the backend and will print to the standard output all the
information that it receives. You can use this sse client typing::

    lupulo_sse_client -help

The second one is a listener mock that will create a fake data link connection
in the backend and will send random data that respects the data schema of your
device. You can read more of this listener in :ref:`listeners`.

The third one is a debug web page that you can access in the */debug* url and
that will build and bind to the web page all the widgets defined in the layout
plus some more information, like the layout for each widget, the raw data
received from the server and the data once it has passed the accessors defined
in the layout.

Deployment
----------

lupulo can be deployed in any GNU/Linux environment that has a proper
installation of python2. The project has been tested on Arch Linux in a
Raspberry Pi B+, but you can use any platform that you want as long as it's
GNU/Linux installed as its OS in it.

Enjoy!
