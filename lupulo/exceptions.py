# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

class NotFoundDescriptor(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Descriptor %s couldn't have been found" % self.name


class NotListenerFound(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Listener %s couldn't have been found" % self.name


class InvalidListener(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Listener %s is not a subclass of twisted Service" % self.name


class RequirementViolated(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class RequiredAttributes(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "The layout %s lacks of required attributes."


class UrlInvalid(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidResource(Exception):
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def __str__(self):
        return "%s class is not a subclass of LupuloResource " \
               "so %s is discarded as a valid url" % (self.name, self.url)
