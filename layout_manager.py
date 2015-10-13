import json

from twisted.python import log


class LayoutManager(object):
    """
        Manages the layout description.
    """
    def __init__(self, fp, schema_manager):
        self.fp = fp
        self.raw = json.load(self.fp)
        # Parent layouts
        self.contexts = {}
        # All events that the widgets can listen to
        self.events = schema_manager.get_events()
        # The compiled layouts
        self.layouts = {}

    def compile(self):
        """
            Transform the layout description into a json object without
            inheritance and with some interesting checks.
        """
        raw_layouts = {}
        required_attributes = set(["event_name", "type"])

        # Classify the objects in abstract or concrete types
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
                    log.msg("%s couldn't be compiled because there was a problem inheriting from %s.", name, obj["parent"])
            else:
                # Without inheritance
                self.layouts[name] = obj

        # Delete a layout if it doesn't have the required attributes or if
        # its event is unknown
        for name, obj in raw_layouts.items():
            broken_attrs = required_attributes.difference(set(raw_layouts[name].keys()))
            if len(broken_attrs) > 0:
                del self.layouts[name]
                log.msg("%s couldn't be compiled because it lacks required arguments %s.", name, ",".join(broken_attrs))
            elif obj["event_name"] not in self.events:
                del self.layouts[name]
                log.msg("%s couldn't be compiled because its event is not in the schema_manager events: %s.", name, ",".join(self.events))


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
        return json.dumps(self.layouts.values())
