import json
from importlib import import_module

from m3dpi_ui.exceptions import NotFoundDescriptor, RequirementViolated


def find_descriptor(klass_name):
    """
        Return the class in the descriptors folder that has as its
        name the argument klass_name
    """
    try:
        module = import_module("m3dpi_ui.descriptors.%s" % klass_name)
    except ImportError as e:
        raise NotFoundDescriptor(e.message.split(" ")[-1])
    return getattr(module, klass_name.capitalize())


class DataSchemaManager(object):
    """
        Validates and generates random data for a data schema.
    """
    def __init__(self, fp):
        """
            @param fp is a file handler of the data schema
            @member desc is the dictionary of the data schema
            @events is a set with all of the events defined in the data schema
        """
        self.fp = fp
        self.desc = json.load(self.fp)
        self.events = set(self.desc.keys())
        self.init_descriptors()

    def init_descriptors(self):
        """
            Initializes @member descriptors as a dictionary indexed by
            each event in @events and its value a class loaded with
            find_descriptor
        """
        self.descriptors = {}
        for key, value in self.desc.items():
            klass = find_descriptor(value["type"])
            try:
                self.descriptors[key] = klass(**value)
            except TypeError:
                raise RequirementViolated("%s description is wrong" % key)

    def validate(self, data):
        """
            Validates the @param data against the data schema using
            the @member descriptors dictionary.
        """
        try:
            jdata = json.loads(data)
        except ValueError:
            return False

        keys = set(jdata.keys())

        try:
            keys.remove("id")
        except KeyError:
            return False

        if len(keys.difference(self.events)) != 0:
            return False

        for key in keys:
            value = jdata[key]
            desc = self.descriptors[key]
            if not desc.validate(value):
                return False

        return True

    def generate(self, id, descriptors=[]):
        """
            Generates random data for the data schema using the
            @member descriptors dictionary.
        """
        if len(descriptors) == 0:
            descriptors = self.descriptors.keys()

        rt = {}
        for name in descriptors:
            if name in self.descriptors:
                descriptor = self.descriptors[name]
                rt[name] = descriptor.generate()
        rt["id"] = id

        return json.dumps(rt)

    def get_events(self):
        return self.descriptors.keys()
