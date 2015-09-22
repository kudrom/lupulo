import json
from importlib import import_module

from m3dpi_ui.exceptions import NotFoundDescriptor

class DataSchemaDescriptor(object):
    def __init__(self, fp):
        self.fp = fp
        self.desc = json.load(self.fp)
        self.events = set(self.desc.keys())
        self.init_descriptors()

    def init_descriptors(self):
        self.descriptors = {}
        for key, value in self.desc.items():
            klass_name = value["type"]
            try:
                module = import_module("m3dpi_ui.descriptors.%s" % klass_name)
            except ImportError as e:
                raise NotFoundDescriptor(e.message.split(" ")[-1])
            klass = getattr(module, klass_name.capitalize())
            self.descriptors[key] = klass(**value)

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
        rt = ""
        for _, descriptor in self.descriptors.items():
            rt += descriptor.generate()

        return rt
