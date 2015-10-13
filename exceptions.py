class NotFoundDescriptor(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Descriptor %s couldn't have been found" % self.name

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
