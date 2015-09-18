from twisted.application import service, internet
from twisted.web import server

from serial_listener import SerialService
from root import get_website
from settings import settings

application = service.Application("m3pdi_ui")
multi = service.MultiService()
multi.setServiceParent(application)

site = get_website()
tcp_server = internet.TCPServer(settings["web_server_port"], site)
tcp_server.setServiceParent(multi)

serial_service = SerialService(sse_resource, settings["serial_device"])
serial_service.setServiceParent(multi)
