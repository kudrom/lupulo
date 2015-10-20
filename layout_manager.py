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
                                "is not in the schema_manager events: %s." %
                                (name, event_name, ",".join(self.events)))
            if 'accessors' in obj:
                for accessor in obj['accessors']:
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

            if delete:
                del self.layouts[name]

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
