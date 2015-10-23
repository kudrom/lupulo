from lupulo.exceptions import RequirementViolated
from lupulo.data_schema_manager import find_descriptor


class List(object):
    """
        Descriptor for a list of a single type of descriptors.
    """
    def __init__(self, length, item_type, **kwargs):
        """
            @length is the length of the list
            @item_type is the type of every item on the list
            @kwargs contains the arguments necessary to construct
                    the delegator for the nested descriptors. These
                    arguments start with "item_"
        """
        if len(item_type) == 0:
            raise RequirementViolated("Requirement of item_type violated.")
        self.length = length
        klass = find_descriptor(item_type)
        kwargs_delegate = dict((item[5:], kwargs[item])
                               for item in kwargs.keys()
                               if item.startswith("item_"))
        self.delegate = klass(**kwargs_delegate)

    def generate(self):
        """
            Generates random data for the descriptor.
            This is called by the DataSchemaManager.generate
        """
        return [self.delegate.generate() for i in range(self.length)]

    def validate(self, data):
        """
            Validates @param data against the descriptor.
            This is called by the DataSchemaManager.validate
            @param data must be a sequence of elements.
        """
        if len(data) != self.length:
            return False
        for obj in data:
            if not self.delegate.validate(obj):
                return False
        return True
