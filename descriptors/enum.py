from random import choice

class Enum(object):
    def __init__(self, values, **kwargs):
        self.values = values

    def generate(self):
        return choice(self.values)

    def validate(self, data):
        return data in self.values
