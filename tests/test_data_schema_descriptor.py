import os.path

from twisted.trial import unittest
from m3dpi_ui.data_schema_descriptor import DataSchemaDescriptor

from m3dpi_ui.settings import settings


class TestsValidFile(unittest.TestCase):
    def setUp(self):
        self.fp = open(os.path.join(settings["cwd"], "tests/descs/valid_desc.json"), "r")
        self.valid_schema_desc = DataSchemaDescriptor(self.fp)

    def tearDown(self):
        self.fp.close()

    def test_invalid_file(self):
        ifp = open(os.path.join(settings["cwd"], "tests/descs/invalid_desc.json"), "r")
        self.assertRaises(ValueError, DataSchemaDescriptor, ifp)
        ifp.close()

    def test_different_keys(self):
        data = '{"different_key": "whatever"}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
