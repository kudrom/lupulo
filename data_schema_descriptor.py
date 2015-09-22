import json


class DataSchemaDescriptor(object):
    def __init__(self, fp):
        self.fp = fp
        data = json.load(self.fp)
        self.events = set(data.keys())
        self.descriptors = self.init_descriptors()

    def init_descriptors(self):
        pass

    def validate(self, data):
        try:
            jdata = json.loads(data)
        except ValueError:
            return False

        keys = set(jdata.keys())
        if len(keys.difference(self.events)) != 0:
            return False

        for key, value in jdata.items():
            desc = self.descriptors[key]
            if not desc.validate(value):
                return False

        return True

    def generate(self):
        pass

