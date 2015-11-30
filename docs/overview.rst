.. _overview:

Getting started
===============

Sometimes you need to develop a web page that displays information in real time.
For example, in order to develop a device which interacts with its environment,
it's usually needed a visualization of the sensory data to properly understand
the behaviour of the device. Or maybe you want to develop a web page to display
the scoreboard of some games, or the temperature of your home in different
rooms or even a control panel to monitor and command a robot.

*Lupulo* is a framework that will help you out to build this kind of web-based
real time user interfaces.

You just need to understand the data you want to display, how it's going to be
transmitted to lupulo and how you want to visualize it. Then you describe it to
the framework and for the rest, lupulo will take care.

Description
-----------

Lupulo is a framework developed in python and javascript used to build
visualizations of data sent in real time. You can quickly build web pages to
display information in real time or to record a session and analyze the data
afterwards. You can also extend the framework very easily to build complex user
interfaces.

Different user interfaces serving different needs for the same data source can
be built very quickly. That way if the data schema or the visualization change
during development, it's quite straightforward to replace the current web page
with one that satisfies the new changes.

Several data sources can be monitored by the same user interface at the same
time as long as all of them follow the same data schema.

With the base installation there are a bunch of *widgets* which can be used from
the beginning to build your web page. Of course, you can also write your own
*widgets* if you need to visualize information in a specific way and plug them
into the framework very easily.

You can also build new data links to connect the framework with the outside
world. You also have the usual tools that any modern web framework provides
like html templates or dynamic sitemaps.

The main idea is to allow the quick development of **standard** web pages to
visualize information in real time but also to provide the necessary complexity
to allow more **personalized** web pages where it's not so necessary to build
quickly a web page but to ease its development providing high level abstractions
for complex requirements.

This way, you can use the default configurations of the framework and use it as
a quick user interface or you can personalize it to build a rich user interface
with all your custom bolts and nuts.

Lupulo has been built to run in a RaspberryPi, but another hardware
configurations are possible as long as GNU/Linux is used to run the backend.

How it works
------------

lupulo is composed of two main components:

* **The backend** which makes the connection with the data source, receives the
  data, records it and sends it back in real time to the frontend.
* **The frontend** which renders the information received by the backend in real
  time in several *widgets* chosen by the programmer of the final web page.

Once lupulo is started, it reads its main configuration from *settings.py*,
where you establish several parameters like the data link between the data
source and the backend, the *data schema* that describes the information
received and a high level description of the web page called *layout*.

Both the layout and the data schema are json files with a specific format
defined in another section of this documentation. With the settings, the layout
and the data schema, you can build your first web page. But you can also define
custom templates, widgets, js files, custom listeners... that will extend the
behaviour of your web page.

The *data schema* is made of descriptors that describe an important source event
in the device. For example, you can have a descriptor for the speed of a robot
and another one for its direction.

The *layout* is made of sections that bind a source event defined in the data
schema to a widget in the web page. For example, for the speed of the
robot you can have two widgets, a line graph that shows the speed of the robot
in the last 90 seconds and a speedometer that displays in a graphical way the
current speed of the robot.

As said above, there are more mechanisms to customize your web site that will
be discussed in the following sections of this documentation, but the layout,
the data schema and the settings file are the descriptions you always need to
define to have a proper lupulo-powered real time web site.

Installation
------------

*lupulo* is a python2 package uploaded to `pip 
<https://pypi.python.org/pypi/lupulo/>`_, so to install it you can type in a
linux console::

    pip install lupulo

Currently only python2 is supported so you need a proper installation of python2
in order to install it.

You also need to have a proper installation of mongodb if you want to store the
information gathered by the backend.

Use
---

In order to launch the lupulo's server, first you must create a valid project.
To do that, you must execute from the project's folder the program
**lupulo_create**. This will create some files and directories similar to this
ones::

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
Raspberry Pi B+, but you can use any platform that you want as long as
GNU/Linux is installed as its OS.

Enjoy!
