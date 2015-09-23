from random import uniform

class Number(object):
    def __init__(self, range, **kwargs):
        self.start = range[0]
        self.end = range[1]

    def generate(self):
        return uniform(self.start, self.end)

    def validate(self, value):
        return value >= self.start and value <= self.end
