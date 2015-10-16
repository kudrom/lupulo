from random import choice


class Enum(object):
    """
        Descriptor for a enum datum
    """
    def __init__(self, values, **kwargs):
        """
            @param values is a list containing the allowed values
                   that the enumeration can have
        """
        self.values = values

    def generate(self):
        """
            Generates random data for the descriptor.
            This is called by the DataSchemaManager.generate
        """
        return choice(self.values)

    def validate(self, data):
        """
            Validates @param data against the descriptor.
            This is called by the DataSchemaManager.validate
        """
        return data in self.values
