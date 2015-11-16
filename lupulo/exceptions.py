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
