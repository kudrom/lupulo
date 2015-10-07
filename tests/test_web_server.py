from twisted.internet import reactor
from twisted.trial import unittest

from m3dpi_ui.sse_resource import SSE_Resource
from m3dpi_ui.root import get_website
from m3dpi_ui.settings import settings

class TestWebServer(unittest.TestCase):
    def setUp(self):
        site = get_website()
        reactor.listenTCP(settings["web_server_port"], site)
