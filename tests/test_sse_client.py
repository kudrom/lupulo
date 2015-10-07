from mock import MagicMock

from twisted.internet import reactor
from twisted.trial import unittest

from m3dpi_ui.settings import settings
from m3dpi_ui.tests.sse_client.sse_client import SSEClient, SSEClientProtocol


class TestWebServer(unittest.TestCase):
    def setUp(self):
        self.protocol = SSEClientProtocol()

    def test_add_callback(self):
        callback1 = MagicMock()
        self.assertEqual(len(self.protocol.callbacks), 0)
        self.protocol.addCallback("random_event", callback1)
        self.assertEqual(len(self.protocol.callbacks), 1)
        self.assertIn('random_event', self.protocol.callbacks)
        self.assertEqual(self.protocol.callbacks['random_event'], callback1)
        callback2 = MagicMock()
        self.protocol.addCallback("random_event", callback2)
        self.assertEqual(self.protocol.callbacks['random_event'], callback2)

    def test_protocol_missing_data(self):
        callback = MagicMock()
        self.protocol.addCallback("random_event", callback)
        self.protocol.lineReceived("event: random_event")
        self.assertEqual(self.protocol.event, "random_event")
        self.protocol.lineReceived("")
        callback.assert_called_once_with("")

    def test_protocol_missing_event(self):
        callback = MagicMock()
        self.protocol.addCallback("message", callback)
        self.protocol.lineReceived("data: random_data")
        self.assertEqual(self.protocol.data, "random_data")
        self.protocol.lineReceived("")
        callback.assert_called_once_with("random_data")

    def test_protocol_invalid_event(self):
        self.protocol.lineReceived("event: random_event")
        self.protocol.lineReceived("")
        self.assertEqual(self.protocol.data, "")
        self.assertEqual(self.protocol.event, "message")

    def test_protocol_valid_data(self):
        callback = MagicMock()
        self.protocol.addCallback("random_event", callback)
        self.protocol.lineReceived("event: random_event")
        self.protocol.lineReceived("data: random_data")
        self.assertEqual(self.protocol.data, "random_data")
        self.assertEqual(self.protocol.event, "random_event")
        self.protocol.lineReceived("")
        callback.assert_called_once_with("random_data")

    def test_no_web_server_without_hanging(self):
        url = 'http://localhost:' + str(settings['web_server_port']) + '/subscribe'
        client = SSEClient(url)
        return client.connect()
