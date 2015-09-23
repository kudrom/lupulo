import datetime
import random

class Date(object):
    def __init__(self, variance, **kwargs):
        self.variance = variance

    def generate(self):
        now = datetime.datetime.now().strftime("%s")
        return int(now) + random.randrange(0, self.variance)

    def validate(self, data):
        return True
