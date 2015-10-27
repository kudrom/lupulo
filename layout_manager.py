import json
from copy import deepcopy

from twisted.python import log
from twisted.python.filepath import FilePath
from twisted.internet.inotify import INotify, humanReadableMask

from lupulo.settings import settings


class LayoutManager(object):
    """
        Manages the layout description.
    """
    def __init__(self, fp, schema_manager):
        self.fp = fp
        self.schema_manager = schema_manager
        self.inotify_callbacks = []
        self.initialize()
        if settings["activate_inotify"]:
            self.setup_inotify()

    def initialize(self):
        # Parent layouts
        self.contexts = {}
        # All events that the widgets can listen to
        self.events = self.schema_manager.get_events()
        # The compiled layouts
        self.layouts = {}

        # Load the layout file and reset the position to allow second reads
        self.raw = json.load(self.fp)
        self.fp.seek(0)

    def compile(self):
        """
            Transform the layout description into a json object without
            inheritance and with some interesting checks.
        """
        self.initialize()

        # Classify the objects in abstract or concrete types
        raw_layouts = {}
        for name, obj in self.raw.items():
            if "abstract" in obj:
                self.contexts[name] = obj
            else:
                raw_layouts[name] = obj

        # Bind the layouts
        for name, obj in raw_layouts.items():
            if "parent" in obj:
                # With inheritance
                if obj["parent"] in self.contexts:
                    self.layouts[name] = self.inherit(obj)
                    del self.layouts[name]["parent"]
                else:
                    log.msg("%s couldn't be compiled because "
                            "there was a problem inheriting from %s." %
                            (name, obj["parent"]))
                    continue
            else:
                # Without inheritance
                self.layouts[name] = obj
            self.layouts[name]["name"] = name

        # Delete a layout if it doesn't have the required attributes or if
        # its event is unknown
        required_attributes = set(["event_names", "type", "anchor", "size"])
        for name, obj in raw_layouts.items():
            delete = False
            broken_attrs = required_attributes.difference(set(obj.keys()))
            if len(broken_attrs) > 0:
                del self.layouts[name]
                log.msg("%s couldn't be compiled because "
                        "it lacks required arguments %s." %
                        (name, ",".join(broken_attrs)))
                # Bypass to avoid KeyError when trying to access an attribute
                # that doesn't exist
                continue
            if 'height' not in obj["size"].keys():
                delete = True
                log.msg("%s doesn't have a height in its size attribute." %
                        name)
            if 'width' not in obj["size"].keys():
                delete = True
                log.msg("%s doesn't have a width in its size attribute." %
                        name)
            if not isinstance(obj["event_names"], list):
                delete = True
                log.msg("%s couldn't be compiled because its event_names"
                        "attribute is not a list." % name)
            if isinstance(obj["event_names"], list):
                for event_name in obj["event_names"]:
                    if event_name not in self.events:
                        delete = True
                        log.msg("%s couldn't be compiled because its event %s"
                                " is not in the schema_manager events: %s." %
                                (name, event_name, ", ".join(self.events)))
            if 'accessors' in obj:
                delete = self.check_acc_desc(obj['accessors'], name, obj)

            if delete:
                del self.layouts[name]

    def check_acc_desc(self, desc, *args):
        delete = False

        if type(desc) is list:
            accessor_list = desc
        elif type(desc) is dict:
            accessor_list = [l[1] for l in desc.items()]
        else:
            log.msg("%s accessor description wasn't a list or a dictionary")

        for accessor in accessor_list:
            delete = self.check_accessor(accessor, *args)

        return delete

    def check_accessor(self, accessor, name, obj):
        delete = False

        if 'type' not in accessor:
            delete = True
            log.msg("%s accessor doesn't have a type property." %
                    name)

        if 'event' not in accessor:
            accessor['event'] = obj['event_names'][0]
        elif accessor['event'] not in obj['event_names']:
            delete = True
            log.msg("%s accessor event property is not in the"
                    " event_names attribute of the layout." % name)

        if 'after' in accessor:
            delete = self.check_acc_desc(accessor['after'], name, obj)

        return delete

    def inherit(self, obj):
        """
            Inherit all the inheritable properties from the obj's parent.
        """
        parent = self.contexts[obj["parent"]]
        if "parent" in parent:
            parent = self.inherit(parent)
        for prop in parent:
            if prop == "abstract" or prop == "parent" or prop in obj:
                continue
            obj[prop] = parent[prop]
        return obj

    def get_widgets(self):
        """
            Return a string of the compiled layout
        """
        obj = {'removed': {}, 'changed': {}, 'added': self.layouts}
        return json.dumps(obj)

    def register_inotify_callback(self, callback):
        self.inotify_callbacks.append(callback)

    def setup_inotify(self):
        self.notifier = INotify()
        self.notifier.startReading()
        filepath = FilePath(self.fp.name)
        self.notifier.watch(filepath, callbacks=[self.inotify])

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
        if 'attrib' in hmask or 'modify' in hmask:
            jdata = {}

            old_layouts = deepcopy(self.layouts)

            # Reload file if some kind of buffering is being used by the editor
            self.fp.close()
            self.fp = open(self.fp.name, 'r')

            self.compile()

            old_keys = set(old_layouts.keys())
            new_keys = set(self.layouts.keys())

            removed_keys = old_keys.difference(new_keys)
            jdata["removed"] = list(removed_keys)

            added_keys = new_keys.difference(old_keys)
            added_layouts = dict((key, layout)
                                 for key, layout in self.layouts.items()
                                 if key in added_keys)
            jdata["added"] = added_layouts

            changed = {}
            for key in new_keys.difference(added_keys):
                if key in old_keys:
                    old_layout = old_layouts[key]
                    new_layout = self.layouts[key]
                    if old_layout != new_layout:
                        changed[key] = new_layout

            jdata["changed"] = changed

            changes = len(removed_keys) + len(added_layouts) + len(changed)

            if changes > 0:
                for callback in self.inotify_callbacks:
                    callback(jdata)
                log.msg("Changes in the layout file.")

        # Some editors move the file and inotify lose track of the file, so the
        # notifier must be restarted when some attribute changed is received.
        if 'attrib' in hmask:
            self.notifier.stopReading()
            self.setup_inotify()
