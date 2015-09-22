import json
from importlib import import_module


class DataSchemaDescriptor(object):
    def __init__(self, fp):
        self.fp = fp
        self.desc = json.load(self.fp)
        self.events = set(self.desc.keys())
        self.init_descriptors()

    def init_descriptors(self):
        self.descriptors = {}
        for key, value in self.desc.items():
            module = import_module("m3dpi_ui.descriptors.%s" % key)
            self.descriptors[key] = getattr(module, key.capitalize())

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
