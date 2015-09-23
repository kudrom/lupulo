from random import uniform

class Number(object):
    """
        Descriptor for a number datum
    """
    def __init__(self, range, **kwargs):
        """
            @param range is a list with two elements which
                   determine the start and end of the allowed
                   values of the descriptor.
        """
        self.start = range[0]
        self.end = range[1]

    def generate(self):
        """
            Generates random data for the descriptor.
            This is called by the DataSchemaManager.generate
        """
        return uniform(self.start, self.end)

    def validate(self, value):
        """
            Validates @param data against the descriptor.
            This is called by the DataSchemaManager.validate
        """
        return value >= self.start and value <= self.end
