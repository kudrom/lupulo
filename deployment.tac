import os.path

from twisted.application import service, internet
from twisted.web import server
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

from m3dpi_ui.serial_listener import SerialService
from m3dpi_ui.sse_resource import SSEResource
from m3dpi_ui.root import get_website
from m3dpi_ui.settings import settings

# Bind the application and create a multi service that will be the
# father of all the services below
application = service.Application("m3pdi_ui")
multi = service.MultiService()
multi.setServiceParent(application)

# Setup logging
logfile = DailyLogFile("deployment.log", os.path.join(settings["cwd"], "log"))
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

# Create the web server and attach it to multi
sse_resource = SSEResource()
site = get_website(sse_resource)
tcp_server = internet.TCPServer(settings["web_server_port"], site)
tcp_server.setServiceParent(multi)

# Create the serial listener and attach it to multi
serial_service = SerialService(sse_resource, settings["serial_device"])
serial_service.setServiceParent(multi)
