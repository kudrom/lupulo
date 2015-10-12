import time
from mock import MagicMock

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.trial import unittest
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from m3dpi_ui.sse_resource import SSEResource
from m3dpi_ui.root import get_website
from m3dpi_ui.settings import settings
from m3dpi_ui.tests.sse_client.sse_client import SSEClient


class TestFunctional(unittest.TestCase):
    def setUp(self):
        self.sse_resource = SSEResource()
        site = get_website(self.sse_resource)
        self.server = reactor.listenTCP(settings["web_server_port"], site)
        self.url = 'http://localhost:' + str(settings['web_server_port']) + '/subscribe'
        self.client = SSEClient(self.url)

    def tearDown(self):
        self.server.stopListening()

    def cleanup_connections(self):
        for sub in list(self.sse_resource.subscribers):
            self.sse_resource.removeSubscriber(sub)

    def http_request(self, url):
        def cbRequest(response):
            self.assertEqual(response.code, 200)

        agent = Agent(reactor)
        d = agent.request(
            'GET',
            url,
            Headers({
                'User-Agent': ['Twisted SSE Client'],
                'Cache-Control': ['no-cache'],
                'Accept': ['text/event-stream; charset=utf-8'],
            }),
            None)
        d.addCallback(cbRequest)
        return d

    def test_connection(self):
        def after_publishing(_):
            self.assertEqual(self.client.cbRequest.called, True)
            self.assertEqual(len(self.sse_resource.subscribers), 1)
            self.cleanup_connections()

        self.client.cbRequest = MagicMock()
        self.assertEqual(len(self.sse_resource.subscribers), 0)
        self.assertEqual(self.client.cbRequest.called, False)
        d = self.client.connect()
        d.addCallback(after_publishing)
        return d

    def test_dispatchEvent(self):
        def after_publishing():
            callback = self.client.protocol.dispatchEvent
            self.assertEqual(callback.called, True)
            self.assertEqual(callback.call_count, 2)
            self.cleanup_connections()

        raise unittest.SkipTest("For some reason this is blocked.")
        self.client.protocol.dispatchEvent = MagicMock()
        d = self.client.connect()
        reactor.callLater(1, self.sse_resource.publish, '{"id" : 1, "battery": 87.156412351}')
        reactor.callLater(2, after_publishing)
        return d

    def test_request_received(self):
        def callback(data):
            contradiction.cancel()
            self.assertEqual(data, 87.1564123)
            self.cleanup_connections()

        self.client.addEventListener("id1-battery", callback)
        d = self.client.connect()
        reactor.callLater(1, self.sse_resource.publish, '{"id" : 1, "battery": 87.156412351}')
        contradiction = reactor.callLater(3, self.assertEqual, True, False)
        return d

    def test_static_files(self):
        url = 'http://localhost:' + str(settings['web_server_port']) + '/static/'
        return self.http_request(url)

    def test_root(self):
        url = 'http://localhost:' + str(settings['web_server_port'])
        return self.http_request(url)
