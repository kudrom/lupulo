from twisted.application import service, internet
from twisted.web import server

from serial_listener import SerialService
from sse_resource import Root, SSE_Resource

application = service.Application("m3pdi_ui")
multi = service.MultiService()
multi.setServiceParent(application)

root = Root()
sse_resource = SSE_Resource()
root.putChild('subscribe', sse_resource)
site = server.Site(root)
tcp_server = internet.TCPServer(8080, site)
tcp_server.setServiceParent(multi)

serial_service = SerialService(sse_resource)
serial_service.setServiceParent(multi)
