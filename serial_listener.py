from twisted.internet import reactor
from twisted.application import service
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort

class SerialListener(Protocol):
    def __init__(self, sse_resource):
        self.sse_resource = sse_resource

    def connectionMade(self):
        print "Connection made"

    def dataReceived(self, data):
        self.sse_resource.publish(data)


class SerialService(service.Service):
    def __init__(self, sse_resource, device='/dev/ttyACM0'):
        self.device = device
        self.sse_resource = sse_resource

    def startService(self):
        self.serial_listener = SerialListener(self.sse_resource)
        self.serial = SerialPort(self.serial_listener, self.device, reactor, baudrate='115200')
