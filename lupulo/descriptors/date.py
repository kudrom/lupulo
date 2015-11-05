import datetime
import random


class Date(object):
    """
        Descriptor for a date datum
    """
    def __init__(self, variance, **kwargs):
        """
            @param variance is the maximum variance of time
                   allowed for the generation of random data.
        """
        self.variance = variance

    def generate(self):
        """
            Generates random data for the descriptor.
            This is called by the DataSchemaManager.generate
        """
        now = datetime.datetime.now().strftime("%s")
        return int(now) + random.randrange(0, self.variance)

    def validate(self, data):
        """
            Validates @param data against the descriptor.
            This is called by the DataSchemaManager.validate
        """
        return True
