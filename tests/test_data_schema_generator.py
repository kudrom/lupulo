import os.path
import json

from twisted.trial import unittest
from mock import patch, MagicMock

from m3dpi_ui.data_schema_manager import DataSchemaManager
from m3dpi_ui.settings import settings
from m3dpi_ui.exceptions import NotFoundDescriptor, RequirementViolated

class TestDataSchemaGenerations(unittest.TestCase):
    def setUp(self):
        self.fp = open(os.path.join(settings["cwd"], "tests/data_schemas/complete.json"), "r")
        self.valid_schema_desc = DataSchemaManager(self.fp)

    def tearDown(self):
        self.fp.close()

    def test_generate_complete(self):
        data = self.valid_schema_desc.generate()
        jdata = json.loads(data)
        self.assertEqual(set(jdata.keys()), set(self.valid_schema_desc.descriptors.keys()))

    def test_generate_partial(self):
        data = self.valid_schema_desc.generate(["battery", "date"])
        jdata = json.loads(data)
        self.assertEqual(["battery", "date"], jdata.keys())

    def test_generate_null(self):
        data = self.valid_schema_desc.generate([])
        jdata = json.loads(data)
        self.assertEqual(set(jdata.keys()), set(self.valid_schema_desc.descriptors.keys()))
        data = self.valid_schema_desc.generate(["nothing"])
        jdata = json.loads(data)
        self.assertEqual(len(jdata), 0)

    def test_generate_list(self):
        data = self.valid_schema_desc.generate(["distances"])
        jdata = json.loads(data)
        self.assertEqual(["distances"], jdata.keys())
        self.assertEqual(len(jdata["distances"]), 8)

    def test_generate_dict(self):
        data = self.valid_schema_desc.generate(["motor"])
        jdata = json.loads(data)
        self.assertEqual(["motor"], jdata.keys())
        self.assertEqual(type(jdata["motor"]), dict)
        self.assertEqual(["turn_radius", "speed"], jdata["motor"].keys())
        self.assertEqual(type(jdata["motor"]["speed"]), float)
        self.assertEqual(type(jdata["motor"]["turn_radius"]), float)

    def test_generate_nested_list_dict(self):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/list_dict.json"), "r")
        dsd = DataSchemaManager(ifp)
        data = dsd.generate()
        jdata = json.loads(data)
        self.assertEqual(set(jdata.keys()), set(["motor"]))
        self.assertEqual(len(jdata["motor"]), 2)
        self.assertEqual(set(jdata["motor"][0].keys()), set(["speed", "turn_radius"]))
        self.assertEqual(set(jdata["motor"][1].keys()), set(["speed", "turn_radius"]))
