from twisted.trial import unittest
from mock import patch, MagicMock

from m3dpi_ui.settings import settings
from m3dpi_ui.listeners_manager import connect_listener, get_listener_name
from m3dpi_ui.exceptions import NotListenerFound


class TestsListenerManager(unittest.TestCase):
    def setUp(self):
        self.old_settings = settings
        self.mock_sse_resource = MagicMock()
        self.mock_parent = MagicMock()

    def tearDown(self):
        settings = self.old_settings

    @patch('m3dpi_ui.listeners.mock_listener.MockListener')
    def test_correct_listener(self, Listener):
        settings['listener'] = 'mock'
        Listener.setServiceParent = MagicMock()

        connect_listener(self.mock_parent, self.mock_sse_resource)
        Listener.assert_called_once_with(self.mock_sse_resource)

    def test_missing_module(self):
        settings['listener'] = 'crap'
        self.assertRaises(NotListenerFound, connect_listener, self.mock_parent,
                self. mock_sse_resource)

    def test_underscore(self):
        name = get_listener_name("something_weird")
        self.assertEqual(name, "SomethingWeirdListener")
