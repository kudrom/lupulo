import json

from twisted.web import server, resource
from twisted.python import log

from m3dpi_ui.data_schema_manager import DataSchemaManager
from m3dpi_ui.settings import settings

class SSE_Resource(resource.Resource):
    """
        Twisted web resource that will work as the SSE server.
    """
    isLeaf = True

    def __init__(self):
        """
            @prop subscribers are the requests which should be updated
            when new information is published to the sse_resource.
        """
        self.subscribers = set()
        fp = open(settings["data_schema"], "r")
        self.data_schema_manager = DataSchemaManager(fp)

    def render_GET(self, request):
        """
            Called when twisted wants to render the page, this method is asynchronous
            and therefore returns NOT_DONE_YET.
        """
        log.msg("SSE connection made by %s" % request.getClientIP())
        request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
        request.setResponseCode(200)
        self.subscribers.add(request)
        d = request.notifyFinish()
        d.addBoth(self.removeSubscriber)
        request.write("")
        return server.NOT_DONE_YET

    def publish(self, data):
        """
            When data arrives it is written to every request which is in the
            subscribers set.
        """
        if self.data_schema_manager.validate(data):
            jdata = json.loads(data)
            try:
                iid = jdata["id"]
            except KeyError:
                log.msg("No id in message %s." % data)
                return

            for subscriber in self.subscribers:
                msg = []
                for event, data in jdata.items():
                    if event == "id":
                        continue
                    msg.append("event: id%d-%s\n" % (iid, event.encode('ascii', 'ignore')))
                    msg.append("data: %s\n\n" % data)
                subscriber.write("".join(msg))

    def removeSubscriber(self, subscriber):
        """
            When the request is finished for some reason, the
            request is finished and the subscriber is removed from the set.
        """
        if subscriber in self.subscribers:
            subscriber.finish()
            self.subscribers.remove(subscriber)
