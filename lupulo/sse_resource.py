# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

import json
from datetime import datetime

from pymongo import MongoClient

from twisted.web import server, resource
from twisted.internet import reactor
from twisted.python import log

from lupulo.data_schema_manager import DataSchemaManager
from lupulo.layout_manager import LayoutManager
from settings import settings


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
        # The device ids who have sent a message through this sse resource
        self.ids = []

        fp = open(settings["data_schema"], "r")
        self.data_schema_manager = DataSchemaManager(fp)
        self.data_schema_manager.register_inotify_callback(self.schema_changed)

        fp = open(settings["layout"], "r")
        self.layout_manager = LayoutManager(fp, self.data_schema_manager)
        self.layout_manager.register_inotify_callback(self.layout_changed)
        self.layout_manager.compile()

        if settings['activate_mongo']:
            self.mongo_client = MongoClient(settings['mongo_host'])
            self.db = self.mongo_client[settings['mongo_db']]

        reactor.addSystemEventTrigger('after', 'shutdown', self.clean_up)

    def clean_up(self):
        log.msg("SSEResource cleanup.")
        self.data_schema_manager.fp.close()
        self.layout_manager.fp.close()

    def removeSubscriber(self, subscriber):
        """
            When the request is finished for some reason, the request is
            finished and the subscriber is removed from the set.
        """
        if subscriber in self.subscribers:
            subscriber.finish()
            self.subscribers.remove(subscriber)

    def render_GET(self, request):
        """
            Called when twisted wants to render the page, this method is
            asynchronous and therefore returns NOT_DONE_YET.
        """
        def wrap(x):
            return '"' + str(x) + '"'

        request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
        request.setResponseCode(200)

        self.subscribers.add(request)
        d = request.notifyFinish()
        d.addBoth(self.removeSubscriber)

        msg = []
        if len(self.ids) > 0:
            msg.append('event: new_devices\n')
            msg.append('data: [%s]\n\n' % ",".join(map(wrap, self.ids)))
            request.write("".join(msg))

        msg = []
        widgets = self.layout_manager.get_widgets()
        msg.append('event: new_widgets\n')
        msg.append('data: %s\n\n' % widgets)
        request.write("".join(msg))

        msg = []
        events = self.data_schema_manager.get_events()
        jdata = json.dumps({'added': events, 'removed': []})
        msg.append('event: new_event_sources\n')
        msg.append('data: %s\n\n' % jdata)
        request.write("".join(msg))

        log.msg("SSE connection made by %s" % request.getClientIP())
        return server.NOT_DONE_YET

    def publish(self, data):
        """
            When data arrives it is written to every request which is in the
            subscribers set.
        """
        if self.data_schema_manager.validate(data):
            jdata = json.loads(data)
            iid = jdata["id"]
            iid_encoded = iid.encode('ascii', 'ignore')

            if settings["activate_mongo"]:
                self.store(data)

            msg = []
            if iid not in self.ids:
                log.msg("New connection from device %s" % iid)
                self.ids.append(iid)
                msg.append('event: new_devices\n')
                msg.append('data: ["%s"]\n\n' % iid_encoded)
            for event, data in jdata.items():
                if event in ["id"]:
                    continue
                event_name = event.encode('ascii', 'ignore')
                msg.append("event: id%s-%s\n" % (iid_encoded, event_name))
                msg.append("data: %s\n\n" % json.dumps(data))

            for subscriber in self.subscribers:
                subscriber.write("".join(msg))

    def store(self, data):
        """
            Store the data in the data collection.
            A string is passed as attribute to avoid pollution of the argument.
        """
        jdata = json.loads(data)
        jdata['timestamp'] = datetime.utcnow()
        self.db.data.insert(jdata)

    def broadcast(self, event_source, data):
        msg = []
        jdata = json.dumps(data)
        msg.append('event: %s\n' % event_source)
        msg.append('data: %s\n\n' % jdata)

        for subscriber in self.subscribers:
            subscriber.write("".join(msg))

    def layout_changed(self, data):
        self.broadcast('new_widgets', data)

    def schema_changed(self, data):
        self.broadcast('new_event_sources', data)
