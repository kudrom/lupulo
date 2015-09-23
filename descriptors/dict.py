from m3dpi_ui.exceptions import RequirementViolated
from m3dpi_ui.data_schema_descriptor import find_data_type

class Dict(object):
    def __init__(self, keys, **kwargs):
        self.delegates = {}
        for item_name in keys:
            kwargs_delegate = dict((item[len(item_name)+1:], kwargs[item])
                                   for item in kwargs.keys()
                                   if item.startswith(item_name + "_"))
            klass = find_data_type(kwargs_delegate["type"])
            self.delegates[item_name] = klass(**kwargs_delegate)

    def generate(self):
        rt = {}
        for name, delegate in self.delegates.items():
            rt[name] = delegate.generate()

        return rt

    def validate(self, data):
        if len(set(data.keys())) != len(set(self.delegates.keys())):
            return False

        for key, value in data.items():
            if key not in self.delegates.keys():
                return False
            if not self.delegates[key].validate(value):
                return False

        return True
