# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

from twisted.internet import reactor
from twisted.application import service
from twisted.protocols.basic import LineReceiver
from twisted.internet.serialport import SerialPort
from twisted.python import log

from settings import settings


class SerialProtocol(LineReceiver):
    """
        The protocol used to receive the data over the serial
        port.
    """
    def __init__(self, sse_resource):
        """
            @prop sse_resource used to publish the data once it arrives
        """
        self.sse_resource = sse_resource
        self.delimiter = '\n'

    def connectionMade(self):
        log.msg("Connection made to the serial port.")

    def lineReceived(self, line):
        """
            Once the data has arrived SerialProtocol publishes it through SSE
        """
        self.sse_resource.publish(line)


class SerialListener(service.Service):
    """
        The service used in the app tac to start the serial listener
    """
    def __init__(self, sse_resource):
        """
            @prop sse_resource is the sse_resource served by the web server
                  it's forwarded to the SerialProtocol
        """
        self.device = settings["serial_device"]
        self.sse_resource = sse_resource

    def startService(self):
        """
            Setup the SerialPort to listen in the proper device.
        """
        self.serial_listener = SerialProtocol(self.sse_resource)
        self.serial = SerialPort(self.serial_listener,
                                 self.device,
                                 reactor,
                                 baudrate='115200')
        log.msg("Service started for the serial listener.")

    def get_serial_port(self):
        """
            Getter for the SerialPort.
        """
        return self.serial
