.. _overview:

Overview
========

The complete documentation is in
`ReadTheDocs <http://m3dpi-ui.readthedocs.org/en/latest/>`_

To develop a device which interacts with its environment, it's usually needed a
visualization of the sensory data in order to understand the behaviour of the
device in the development stages.

Once a prototype of the device has been built, it's usually also needed a rich 
user interface to command it and also to track its progress in a more realistic
deployment.

m3dpi_ui is a framework that allows you to build several web-based user
interfaces that will allow you to understand much better the device you are
building with some visualization of the sensory information and also to build
rich user interfaces to command it with all the relevant information at sight.

You just need to understand how the data is going to be sent from your device
and how you want to visualize it at a web page. For the rest, m3dpi_ui will take
care.

Description
-----------

m3dpi_ui is a framework built in python and javascript to build visualizations
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
world and plug them into m3dpi_ui. This way, you can use the default
configurations of the framework and use it as a quick user interface to
understand better your device or you can personalize it to build a rich user
interface.

m3dpi_ui has been built to run in a RaspberryPi, but another hardware
configurations are possible as long as GNU/Linux is used to run the backend.

How it works
------------

m3dpi_ui is composed of two main components:

* **The backend** which makes the connection with the device, receives the data
  sent by the device, records it and sends it back in real time to the frontend.
* **The frontend** which renders the information received by the backend in real
  time in several *widgets* chosen by the programmer of the final web page.

m3dpi_ui is configured in *settings.py*, where you establish the data link
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

Installation
------------

Currently there is a script in bash that install all the dependencies and
configures the environment but it only works on distributions of GNU/Linux that
derive from **Arch Linux**.

To install m3dpi_ui just type with superuser permissions::

    ./install.sh

Use
---

The backend is built using twisted and therefore defined in a tac file.
Therefore you can use all the fine tunning that twistd provides to run a
server.

For the moment, you need superuser permissions to execute some listeners in the
tac file. You also need to launch the twistd proccess from the **folder which
contains the directory of the project**.

**See the settings first before launching the server.**

If you are not familiar with twistd, to run any of the tac files in the
foreground you need to type::

    twistd -ny m3dpi_ui/startup.tac

to run the application in the background type::

    twistd -n m3dpi_ui/startup.tac

Debugging
---------

m3dpi_ui also provides some utilities to debug the web page.

The first one is a sse client that will allow you to listen to the information
that the backend is sending to your web page. The sse client will create a sse
connection towards the backend and will print to the standard output all the
information that it receives. You can use this sse client typing::

    m3dpi_ui/tests/sse_client/standalone.py

The second one is a listener mock that will create a fake data link connection
in the backend and will send random data that respects the data schema of your
device. That way you can test how the web page looks without the need of a real
robot sending information. You can use this mock typing::

    twistd -ny m3dpi_ui/mock.py

Enjoy!
