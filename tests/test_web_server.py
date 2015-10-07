from mock import MagicMock

from twisted.internet import reactor
from twisted.trial import unittest

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

    def tearDown(self):
        self.server.stopListening()

    def test_connection(self):
        def after_publishing():
            self.assertEqual(client.cbRequest.called, True)
            self.sse_resouce.remove_subscriber(self.sse_resource.subscribers[0])

        client = SSEClient(self.url)
        client.cbRequest = MagicMock()
        d = client.connect()
        self.assertEqual(len(self.sse_resouce.subscribers), 1)
        #reactor.callLater(1, self.sse_resource.publish, '{"id" :1, "battery": 87.156412351}')
        #reactor.callLater(4, after_publishing)
        return d

    def test_web_server(self):
        raise unittest.SkipTest("Could crash")
        callback = MagicMock()
        def assert_is_called_with_correct_value():
            self.assertEqual(callback.called, True)
            callback.assert_called_with(87.156412351)
            client.finished.callback()
        def callback(data):
            pass
        reactor.callLater(3, self.sse_resource.publish, '{"id" :1, "battery": 87.156412351}')
        reactor.callLater(5, assert_is_called_with_correct_value)
        return client.d
