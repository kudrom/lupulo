from twisted.application import service, internet
from twisted.web import server

from m3dpi_ui.sse_resource import SSE_Resource
from m3dpi_ui.root import get_website
from m3dpi_ui.settings import settings
from m3dpi_ui.tests.mock_serial_listener import MockSerialListener

# Bind the application and create a multi service that will be the
# father of all the services below
application = service.Application("m3pdi_ui")
multi = service.MultiService()
multi.setServiceParent(application)

# Create the web server and attach it to multi
sse_resource = SSE_Resource()
site = get_website(sse_resource)
tcp_server = internet.TCPServer(settings["web_server_port"], site)
tcp_server.setServiceParent(multi)

# Create the serial listener and attach it to multi
mock_serial_listener = MockSerialListener(sse_resource)
mock_serial_listener.setServiceParent(multi)
