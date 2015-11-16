.. _listeners:

Listeners
=========

In order to connect the backend to your device, you can build your own listener
that will retransmit to the backend the data it receives. A listener is a
twisted service that will be run in the tac file when the application runs.

The listener should define some attributes in the main settings.py file of the
project and read them whenever it wants to allow the user of the listener to
configure it from a configuration file.

.. warning::

    In order to use the settings file, the listener must import from the
    settings module of the project, and not from the settings module of lupulo.

.. warning::

    The listener must be placed in a valid module in the root directory of the
    project called listeners. Every listener must finish the filename with
    **_listener.py** and each class with **Listener**.

Once the data arrives to the listener, it needs first to convert it to a valid
JSON string. Afterwards the listener must notify the backend that some
interesting data has arrived through an object called an sse resource.

An sse resource is an object with a method called *publish*.

.. function:: publish(data)

    Send the JSON data to the frontend if it's valid.

    :param str data: JSON string with the data sent by the device.


If the JSON string is not valid, it's automatically discarded by the sse
resource and therefore is not sent to the frontend.

So, a listener should react asynchronously to the events the device is
sending, translate them to a JSON string and publish it to the sse resource.

.. note::

    Some listeners use some special resources of the system, so in order to run
    the server you first need to grant access to that permissions to the user
    that is going to execute the server.

The programmer of the web page defines the listener that the backend is going to
listen to with the *listener* keyword in the settings file of the project. The
value for this property of the settings dictionary is the name of the listener
class that you want to use without the Listener part attached to it. Read below
for some examples.

Now, I'll explain some specific behaviour you should know about some listeners
if you want to use them.

MockListener
------------

As explained in the :ref:`debugging` section of the :ref:`overview`, you can use
a debugging listener that will send random information to the frontend to debug
the web page without a real device attached to the machine running the
framework.  That way you can build up your web page even when you don't have a
prototype to attach the web page to.

This listener defines two properties in the settings file::

    settings['listener'] = 'mock'
    settings['mock_timeout'] = 1
    settings['mock_ids'] = 2

The *mock_timeout* defines how many seconds it has to wait in order to send some
information to the backend. The *mock_ids* defines how many devices it's going
to fake. As explained above, the listener keyword defines which listener to use.

SerialListener
--------------

The serial listener needs access to read and write to the device file of the
serial port. In order to grant access, you need to know what user group the
device file is mounted with and then to add the user to that user group. If the
name of the device is /dev/ttyACM0, you can type::

    usermod -a -G $(stat -c "%G" /dev/ttyACM0) $USER

If you don't like the user group of the device file, you can write your own udev
rule for the serial device.

The serial listener only defines one setting in the settingss file for the name
of this serial device under the key *serial_device*. For example::

    settings['listener'] = 'serial'
    settings['serial_device'] = '/dev/ttyACM0'

Finally, it can be very useful to debug the web page without a real device. Most
of the time you should use the MockListener described above, but some times it
can be very useful to debug the serial connection itself with socat, which can
create two pseudo terminals that behave like two serial ports connected between
them with the command::

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

This will return the created file devices. You can use then *echo* to write to
the device with a JSON format and the framework will read that information.
