import json
import pprint

from twisted.python import log


class LayoutManager(object):
    def __init__(self, fp, schema_manager):
        self.fp = fp
        self.raw = json.load(self.fp)
        self.contexts = {}
        self.events = schema_manager.get_events()
        self.layouts = {}

    def compile(self):
        raw_layouts = {}
        for name, obj in self.raw.items():
            if "abstract" in obj:
                self.contexts[name] = obj

        for name, obj in raw_layouts.items():
            if "parent" in obj and obj["parent"] in self.contexts:
                self.layouts[name] = self.inherit(obj)
                del self.layouts[name]["parent"]
            else:
                log.msg("%s couldn't be compiled because %s is not an abstract layout.", name, obj["parent"])

    def inherit(self, obj):
        parent = self.contexts[obj["parent"]]
        if "parent" in parent:
            parent = inherit(parent)
        for prop in parent:
            if prop == "abstract" or prop == "parent" or prop in obj:
                continue
            obj[prop] = parent[prop]
        return obj

    def get_widgets(self):
        pprint.pprint(self.layouts)
        return json.dumps(self.layouts)
