from twisted.internet import reactor
from twisted.application import service
from twisted.internet.protocol import Protocol
from twisted.internet.serialport import SerialPort

class SerialListener(Protocol):
    def connectionMade(self):
        print "Connection made"

    def dataReceived(self, data):
        print data


class SerialService(service.Service):
    def __init__(self, device='/dev/ttyACM0'):
        self.device = device

    def startService(self):
        self.serial = SerialPort(SerialListener(), self.device, reactor, baudrate='115200')
