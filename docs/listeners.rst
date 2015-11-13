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
