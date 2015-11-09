#! /usr/bin/env python2

import sys
import os
import imp
import json

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.protocols.basic import LineReceiver


class SSEClientProtocol(LineReceiver):
    """
        The protocol who calls back when a data stream
        is received for a particular event.
    """
    def __init__(self):
        self.callbacks = {}
        # The finished deferred must be set from the outside
        self.finished = None
        self.delimiter = '\n'
        # Initialize the event and data buffers
        self.event = 'message'
        self.data = ''

    def addCallback(self, event, func):
        """
            Only one callback per event is allowed.
        """
        self.callbacks[event] = func

    def removeCallback(self, event):
        del self.callbacks[event]

    def lineReceived(self, line):
        if line == '':
            self.dispatchEvent()
        else:
            try:
                field, value = line.split(':', 1)
            except ValueError:
                return
            if field == 'data':
                self.data += value[1:]
            elif field == 'event':
                self.event = value[1:]

    def connectionLost(self, reason):
        if self.finished:
            self.finished.callback(None)

    def dispatchEvent(self):
        if self.event in self.callbacks:
            self.callbacks[self.event](self.data)
        self.data = ''
        self.event = 'message'


class SSEClient(object):
    """
    The client who connects to the SSE server and delegates the
    parsing of the data received to SSEClientProtocol
    """
    def __init__(self, url):
        self.url = url
        self.protocol = SSEClientProtocol()

    def connect(self):
        """
        Connect to the event source URL
        """
        agent = Agent(reactor)
        self.d = agent.request(
            'GET',
            self.url,
            Headers({
                'User-Agent': ['Twisted SSE Client'],
                'Cache-Control': ['no-cache'],
                'Accept': ['text/event-stream; charset=utf-8'],
            }),
            None)
        self.d.addErrback(self.connectError)
        self.d.addCallback(self.cbRequest)
        return self.d

    def cbRequest(self, response):
        """
            Callback for self.d
        """
        if response is not None:
            finished = Deferred()
            self.protocol.finished = finished
            response.deliverBody(self.protocol)
            return finished

    def connectError(self, ignored):
        """
            Errback for self.d
        """
        # This class should be used in testing, so no logging is configured
        print ignored.getErrorMessage()

    def addEventListener(self, event, callback):
        self.protocol.addCallback(event, callback)

    def delEventListener(self, event):
        self.protocol.removeCallback(event)


if __name__ == '__main__':
    """
        Used by lupulo_sse_client.
    """
    def onmessage(event_source, device):
        def aux(data):
            print '%s got payload with data %s from device %d' \
                  % (event_source, data, device)

        return aux

    def new_event_sources(jdata):
        data = json.loads(jdata)

        for event_source in data['added']:
            for device in devices:
                complete_event_source = "id%d-%s" % (device, event_source)
                client.addEventListener(complete_event_source,
                                        onmessage(event_source, device))

        for event_source in data['removed']:
            for device in devices:
                complete_event_source = "id%d-%s" % (device, event_source)
                client.delEventListener(complete_event_source)

    def new_devices(jdata):
        global devices

        data = json.loads(jdata)
        devices = devices + data

    # global variable for the script
    devices = []

    try:
        path = os.path.join(os.getcwd(), 'settings.py')
        settings = imp.load_source('settings', path)
    except IOError:
        print "lupulo_sse_client was executed in a directory which doesn't" \
              " contain a valid lupulo project."
        sys.exit(-1)

    try:
        port = str(settings.settings['web_server_port'])
    except AttributeError:
        print "settings file doesn't contain web_server_port setting"
        sys.exit(-1)

    URL = 'http://localhost:' + port + '/subscribe'
    client = SSEClient(URL)
    client.addEventListener("new_event_sources", new_event_sources)
    client.addEventListener("new_devices", new_devices)
    client.connect()
    reactor.run()
