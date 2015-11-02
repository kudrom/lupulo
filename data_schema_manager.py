import json
from importlib import import_module

from twisted.python import log
from twisted.internet.inotify import humanReadableMask

from lupulo.exceptions import NotFoundDescriptor, RequirementViolated
from lupulo.inotify_observer import INotifyObserver


def find_descriptor(klass_name):
    """
        Return the class in the descriptors folder that has as its
        name the argument klass_name
    """
    try:
        module = import_module("lupulo.descriptors.%s" % klass_name)
    except ImportError as e:
        raise NotFoundDescriptor(e.message.split(" ")[-1])
    return getattr(module, klass_name.capitalize())


class DataSchemaManager(INotifyObserver):
    """
        Validates and generates random data for a data schema.
    """
    def __init__(self, fp):
        """
            @param fp is a file handler of the data schema
            @member desc is the dictionary of the data schema
            @events is a set with all of the events defined in the data schema
        """
        super(DataSchemaManager, self).__init__(fp)
        self.fp = fp
        self.compile()

    def compile(self):
        """
            Initializes @member descriptors as a dictionary indexed by
            each event in @events and its value a class loaded with
            find_descriptor
        """
        self.desc = json.load(self.fp)

        self.events = set(self.desc.keys())

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

    def inotify(self, ignored, filepath, mask):
        """
            Callback for the INotify. It should call the sse resource with the
            changed layouts in the layout file if there are changes in the
            layout file.
        """
        hmask = humanReadableMask(mask)

        # Some editors move the file triggering several events in inotify. All
        # of them change some attribute of the file, so if that event happens,
        # see if there are changes and alert the sse resource in that case.
        # TODO: Abstract this calls chain
        if 'attrib' in hmask or 'modify' in hmask:
            old_descs = set(self.desc.keys())

            self.fp.close()
            self.fp = open(self.fp.name, 'r')
            self.fp.seek(0)

            self.compile()
            new_descs = set(self.desc.keys())

            added_descs = new_descs.difference(old_descs)
            removed_descs = old_descs.difference(new_descs)

            jdata = {}
            jdata['added'] = list(added_descs)
            jdata['removed'] = list(removed_descs)

            print added_descs, removed_descs

            changes = len(added_descs) + len(removed_descs)
            if changes > 0:
                for callback in self.inotify_callbacks:
                    callback(jdata)
                log.msg("Change in data schema.")

        # Some editors move the file and inotify lose track of the file, so the
        # notifier must be restarted when some attribute changed is received.
        if 'attrib' in hmask:
            self.notifier.stopReading()
            self.setup_inotify()
