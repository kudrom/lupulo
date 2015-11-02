import os.path
import json

from twisted.trial import unittest

from lupulo.data_schema_manager import DataSchemaManager
from lupulo.settings import settings


class TestDataSchemaGenerations(unittest.TestCase):
    def setUp(self):
        test = "tests/backend/data_schemas/complete.json"
        self.fp = open(os.path.join(settings["cwd"], test), "r")
        self.old_inotify = settings['activate_inotify']
        settings['activate_inotify'] = False
        self.valid_schema_desc = DataSchemaManager(self.fp)

    def tearDown(self):
        self.fp.close()
        settings['activate_inotify'] = self.old_inotify

    def test_generate_complete(self):
        data = self.valid_schema_desc.generate(1)
        jdata = json.loads(data)
        valid_keys = set(self.valid_schema_desc.descriptors.keys())
        valid_keys.add("id")
        self.assertEqual(set(jdata.keys()), valid_keys)

    def test_generate_partial(self):
        data = self.valid_schema_desc.generate(1, ["battery", "date"])
        jdata = json.loads(data)
        self.assertEqual(["battery", "date", "id"], jdata.keys())

    def test_generate_null(self):
        data = self.valid_schema_desc.generate([])
        jdata = json.loads(data)
        valid_keys = set(self.valid_schema_desc.descriptors.keys())
        valid_keys.add("id")
        self.assertEqual(set(jdata.keys()), valid_keys)
        data = self.valid_schema_desc.generate(1, ["nothing"])
        jdata = json.loads(data)
        self.assertEqual(jdata.keys(), ["id"])

    def test_generate_list(self):
        data = self.valid_schema_desc.generate(1, ["distances"])
        jdata = json.loads(data)
        self.assertEqual(set(["distances", "id"]), set(jdata.keys()))
        self.assertEqual(len(jdata["distances"]), 8)

    def test_generate_dict(self):
        data = self.valid_schema_desc.generate(1, ["motor"])
        jdata = json.loads(data)
        self.assertEqual(set(["motor", "id"]), set(jdata.keys()))
        self.assertEqual(type(jdata["motor"]), dict)
        self.assertEqual(set(["turn_radius", "speed"]),
                         set(jdata["motor"].keys()))
        self.assertEqual(type(jdata["motor"]["speed"]), float)
        self.assertEqual(type(jdata["motor"]["turn_radius"]), float)

    def test_generate_nested_list_dict(self):
        test = "tests/backend/data_schemas/list_dict.json"
        ifp = open(os.path.join(settings["cwd"], test), "r")
        dsd = DataSchemaManager(ifp)
        data = dsd.generate(1)
        jdata = json.loads(data)
        self.assertEqual(set(jdata.keys()), set(["motor", "id"]))
        self.assertEqual(len(jdata["motor"]), 2)
        self.assertEqual(set(jdata["motor"][0].keys()),
                         set(["speed", "turn_radius"]))
        self.assertEqual(set(jdata["motor"][1].keys()),
                         set(["speed", "turn_radius"]))
