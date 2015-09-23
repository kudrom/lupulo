import json
from importlib import import_module

from m3dpi_ui.exceptions import NotFoundDescriptor, RequirementViolated

def find_data_type(klass_name):
    try:
        module = import_module("m3dpi_ui.descriptors.%s" % klass_name)
    except ImportError as e:
        raise NotFoundDescriptor(e.message.split(" ")[-1])
    return getattr(module, klass_name.capitalize())

class DataSchemaDescriptor(object):
    def __init__(self, fp):
        self.fp = fp
        self.desc = json.load(self.fp)
        self.events = set(self.desc.keys())
        self.init_descriptors()

    def init_descriptors(self):
        self.descriptors = {}
        for key, value in self.desc.items():
            klass = find_data_type(value["type"])
            try:
                self.descriptors[key] = klass(**value)
            except TypeError:
                raise RequirementViolated("%s description is wrong" % key)

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

    def generate(self, descriptors=[]):
        if len(descriptors) == 0:
            descriptors = self.descriptors.keys()

        rt = {}
        for name in descriptors:
            if name in self.descriptors:
                descriptor = self.descriptors[name]
                rt[name] = descriptor.generate()

        return json.dumps(rt)
