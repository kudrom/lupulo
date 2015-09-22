class NotFoundDescriptor(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Descriptor %s couldn't been found" % self.name
