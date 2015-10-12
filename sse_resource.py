import json
from datetime import datetime

from pymongo import MongoClient

from twisted.web import server, resource
from twisted.internet import reactor
from twisted.python import log

from m3dpi_ui.data_schema_manager import DataSchemaManager
from m3dpi_ui.layout_manager import LayoutManager
from m3dpi_ui.settings import settings

class SSEResource(resource.Resource):
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
        # The robot ids who have sent a message through this sse resource
        self.ids = []

        self.schema_fp = open(settings["data_schema"], "r")
        self.data_schema_manager = DataSchemaManager(self.schema_fp)

        self.widgets_fp = open(settings["layout"], "r")
        self.layout_manager = LayoutManager(self.widgets_fp, self.data_schema_manager)
        self.layout_manager.compile()

        self.mongo_client = MongoClient(settings['mongo_host'])
        self.db = self.mongo_client[settings['mongo_db']]

        reactor.addSystemEventTrigger('after', 'shutdown', self.clean_up)

    def clean_up(self):
        log.msg("SSEResource cleanup.")
        self.schema_fp.close()
        self.widgets_fp.close()

    def render_GET(self, request):
        """
            Called when twisted wants to render the page, this method is asynchronous
            and therefore returns NOT_DONE_YET.
        """
        def wrap(x):
            return '"' + str(x) + '"'
        log.msg("SSE connection made by %s" % request.getClientIP())
        request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
        request.setResponseCode(200)
        self.subscribers.add(request)
        d = request.notifyFinish()
        d.addBoth(self.removeSubscriber)
        msg = []
        widgets = self.layout_manager.get_widgets()
        msg.append('event: new_widgets\n')
        msg.append('data: %s\n\n' % widgets)
        request.write("".join(msg))
        msg = []
        if len(self.ids) > 0:
            msg.append('event: new_robots\n')
            msg.append('data: [%s]\n\n' % ",".join(map(str, self.ids)))
            request.write("".join(msg))
        return server.NOT_DONE_YET

    def store(self, data):
        """
            Store the data in the data collection.
            A string is passed as attribute to avoid pollution of the argument.
        """
        jdata = json.loads(data)
        jdata['timestamp'] = datetime.utcnow()
        self.db.data.insert(jdata)

    def publish(self, data):
        """
            When data arrives it is written to every request which is in the
            subscribers set.
        """
        if self.data_schema_manager.validate(data):
            jdata = json.loads(data)
            iid = jdata["id"]

            if settings["activate_mongo"]:
                self.store(data)

            msg = []
            if not iid in self.ids:
                log.msg("New connection from robot %d" % iid)
                self.ids.append(iid)
                msg.append('event: new_robots\n')
                msg.append('data: [%d]\n\n' % iid)
            for event, data in jdata.items():
                if event in ["id"]:
                    continue
                msg.append("event: id%d-%s\n" % (iid, event.encode('ascii', 'ignore')))
                msg.append("data: %s\n\n" % json.dumps(data))

            for subscriber in self.subscribers:
                subscriber.write("".join(msg))

    def removeSubscriber(self, subscriber):
        """
            When the request is finished for some reason, the request is
            finished and the subscriber is removed from the set.
        """
        if subscriber in self.subscribers:
            subscriber.finish()
            self.subscribers.remove(subscriber)
