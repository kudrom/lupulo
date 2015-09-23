from m3dpi_ui.exceptions import RequirementViolated
from m3dpi_ui.data_schema_descriptor import find_data_type


class List(object):
    def __init__(self, length, item_type, **kwargs):
        if len(item_type) == 0:
            raise RequirementViolated("Requirement of item_type violated for list")
        self.length = length
        klass = find_data_type(item_type)
        kwargs_delegate = dict((item[5:], kwargs[item])
                               for item in kwargs.keys()
                               if item.startswith("item_"))
        self.delegate = klass(**kwargs_delegate)

    def generate(self):
        return [self.delegate.generate() for i in range(self.length)]

    def validate(self, data):
        if len(data) != self.length:
            return False
        for obj in data:
            if not self.delegate.validate(obj):
                return False
        return True
