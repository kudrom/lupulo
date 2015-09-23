from m3dpi_ui.exceptions import RequirementViolated
from m3dpi_ui.data_schema_manager import find_descriptor

class Dict(object):
    """
        Descriptor for a dictionary of other descriptors
    """
    def __init__(self, keys, **kwargs):
        """
            @param keys is a list containing the keys of the dict
            @param kwargs will contain the necessary arguments to
                   construct each descriptor of the dict. These
                   arguments start with the name of the key.
        """
        self.delegates = {}
        for item_name in keys:
            kwargs_delegate = dict((item[len(item_name)+1:], kwargs[item])
                                   for item in kwargs.keys()
                                   if item.startswith(item_name + "_"))
            klass = find_descriptor(kwargs_delegate["type"])
            self.delegates[item_name] = klass(**kwargs_delegate)

    def generate(self):
        """
            Generates random data for the descriptor.
            This is called by the DataSchemaManager.generate
        """
        rt = {}
        for name, delegate in self.delegates.items():
            rt[name] = delegate.generate()

        return rt

    def validate(self, data):
        """
            Validates @param data against the descriptor.
            This is called by the DataSchemaManager.validate
            @param data must be a dictionary.
        """
        if len(set(data.keys())) != len(set(self.delegates.keys())):
            return False

        for key, value in data.items():
            if key not in self.delegates.keys():
                return False
            if not self.delegates[key].validate(value):
                return False

        return True
