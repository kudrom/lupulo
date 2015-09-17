from twisted.application import service
from serial_listener import SerialService

application = service.Application("m3pdi_ui")

serial_service = SerialService()
serial_service.setServiceParent(application)
