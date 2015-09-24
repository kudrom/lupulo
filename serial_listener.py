from twisted.internet import reactor
from twisted.application import service
from twisted.protocols.basic import LineReceiver
from twisted.internet.serialport import SerialPort

class SerialListener(LineReceiver):
    """
        The protocol used to receive the data over the serial
        port.
    """
    def __init__(self, sse_resource):
        """
            @prop sse_resource used to publish the data once it arrives
        """
        self.sse_resource = sse_resource

    def connectionMade(self):
        print "Connection made to the serial port"

    def lineReceived(self, line):
        """ Once the data has arrived it publishes it through SSE"""
        self.sse_resource.publish(line)


class SerialService(service.Service):
    """
        The service used in the app tac to start the serial listener
    """
    def __init__(self, sse_resource, device):
        """
            @prop device is the name of the serial device file
            @prop sse_resource is the sse_resource served by the web server
                  it's forwarded to the SerialListener
        """
        self.device = device
        self.sse_resource = sse_resource

    def startService(self):
        """
            Setup the SerialPort to listen in the proper device.
        """
        self.serial_listener = SerialListener(self.sse_resource)
        self.serial = SerialPort(self.serial_listener, self.device, reactor, baudrate='115200')
