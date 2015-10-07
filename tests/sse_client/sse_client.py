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
        self.finished = None
        # Initialize the event and data buffers
        self.event = 'message'
        self.data = ''
        self.delimiter = '\n'

    def addCallback(self, event, func):
        """
            Only one callback per event is allowed.
        """
        self.callbacks[event] = func

    def lineReceived(self, line):
        if line == '':
            self.dispatchEvent()
        else:
            try:
                field, value = line.split(':', 1)
            except ValueError:
                return
            if field == 'data':
                self.data += value
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
    The client who connects to the SSE server
    """
    def __init__(self, url):
        self.url = url
        self.protocol = SSEClientProtocol()

    def connect(self):
        """
        Connect to the event source URL
        """
        agent = Agent(reactor)
        d = agent.request(
            'GET',
            self.url,
            Headers({
                'User-Agent': ['Twisted SSE Client'],
                'Cache-Control': ['no-cache'],
                'Accept': ['text/event-stream; charset=utf-8'],
            }),
            None)
        d.addErrback(self.connectError)
        d.addCallback(self.cbRequest)

    def cbRequest(self, response):
        finished = Deferred()
        self.protocol.finished = finished
        response.deliverBody(self.protocol)
        return finished

    def connectError(self, ignored):
        print "The sse_client couldn't connect to the sse_server"

    def addEventListener(self, event, callback):
        self.protocol.addCallback(event, callback)
