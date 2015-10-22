Listeners
=========

In order to connect the backend to your device, you can build your own listener
that will retransmit to the backend the data it receives. A listener is a
twisted service that will be run in the tac file when the application runs.

Currently the listener must be in the listeners file of the main project
directory.

The listener should define some attributes in the main settings.py file of the
project and read them whenever it wants to allow the user of the listener to
configure it from a configuration file.

Once the data arrives to the listener, it needs first to convert it to a valid
JSON string. Afterwards the listener must notify the backend that some
interesting data has arrived through an object called an sse resouce.

An sse resource is an object with a method called *publish*.

.. function:: publish(data)

    Send the JSON data to the frontend if it's valid.

    :param str data: JSON string with the data sent by the device.


If the JSON string is not valid, it's automatically discarded and therefore is
not sent to the frontend.

So, to sum up, a listener should react asynchronously to the events the device
is sending, translate to a JSON string the data it receives and publish it to
the sse resource.
