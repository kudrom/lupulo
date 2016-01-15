# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

from importlib import import_module

from twisted.application import service

from settings import settings
from lupulo.exceptions import NotListenerFound, InvalidListener


class ListenersManager(object):
    def __init__(self):
        self.listener = None

    def get_listener_name(self, name_listener):
        """
            Transforms the name_listener into CamelCase and adds the Listener to
            the end.
        """
        name_splitted = name_listener.split("_")
        CamelCase = "".join(map(lambda x: x.capitalize(), name_splitted))
        return CamelCase + "Listener"

    def connect_listener(self, parent, sse_resource):
        """
            Load, instantiate and registers a Listener.
        """
        module_name = settings["listener"] + "_listener"
        try:
            # Import from global scope listeners
            module = import_module("lupulo.listeners.%s" % module_name)
        except ImportError as e:
            try:
                # Import from project scope listeners
                module = import_module("listeners.%s" % module_name)
            except ImportError:
                raise NotListenerFound(e.message.split(" ")[-1])

        # Find the Listener class
        listener_name = self.get_listener_name(settings["listener"])
        try:
            Listener = getattr(module, listener_name)
        except AttributeError as e:
            raise NotListenerFound(e.message.split(" ")[-1])

        if not issubclass(Listener, service.Service):
            raise InvalidListener(Listener.__name__)

        # Instantiate it and register towards the application
        self.listener = Listener(sse_resource)
        self.listener.setServiceParent(parent)
        return self.listener

    def get_actual_listener(self):
        """
            Return the listener configured in the settings file.
        """
        return self.listener

listeners_manager = ListenersManager()
