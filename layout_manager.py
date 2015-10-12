import json


class LayoutManager(object):
    def __init__(self, fp, schema_manager):
        self.fp = fp
        self.desc = json.load(self.fp)
        self.events = schema_manager.get_events()

    def get_widgets(self):
        return json.dumps(self.desc)
