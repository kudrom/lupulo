from twisted.application import service, internet
from twisted.web import server

from serial_listener import SerialService
from sse_resource import SSE_Resource
from webpage import Root
from settings import settings

application = service.Application("m3pdi_ui")
multi = service.MultiService()
multi.setServiceParent(application)

root = Root()
sse_resource = SSE_Resource()
root.putChild('subscribe', sse_resource)
site = server.Site(root)
tcp_server = internet.TCPServer(settings["web_server_port"], site)
tcp_server.setServiceParent(multi)

serial_service = SerialService(sse_resource, settings["serial_device"])
serial_service.setServiceParent(multi)
