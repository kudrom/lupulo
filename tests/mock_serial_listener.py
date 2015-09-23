from random import choice, randint

from twisted.application import service
from twisted.internet.task import LoopingCall

from m3dpi_ui.settings import settings
from m3dpi_ui.data_schema_manager import DataSchemaManager

class MockSerialListener(service.Service):
    def __init__(self, sse_resource):
        self.sse_resource = sse_resource
        self.loop = LoopingCall(self.timer_callback)
        fp = open(settings["data_schema"], "r")
        self.data_schema_manager = DataSchemaManager(fp)
        self.events = set(self.data_schema_manager.descriptors.keys())

    def startService(self):
        self.loop.start(settings["serial_mock_timeout"])

    def timer_callback(self):
        num = randint(0, len(self.events))
        current_events = set()
        for i in range(num):
            current_events.add(choice(list(self.events.difference(current_events))))

        message = self.data_schema_manager.generate(current_events)
        self.sse_resource.publish(message)
