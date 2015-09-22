import os.path

from twisted.trial import unittest

from m3dpi_ui.data_schema_descriptor import DataSchemaDescriptor
from m3dpi_ui.settings import settings
from m3dpi_ui.exceptions import NotFoundDescriptor


class TestsSchemaDescriptor(unittest.TestCase):
    def setUp(self):
        self.fp = open(os.path.join(settings["cwd"], "tests/descs/complete.json"), "r")
        self.valid_schema_desc = DataSchemaDescriptor(self.fp)

    def tearDown(self):
        self.fp.close()

    def test_invalid_file(self):
        ifp = open(os.path.join(settings["cwd"], "tests/descs/invalid_syntax.json"), "r")
        self.assertRaises(ValueError, DataSchemaDescriptor, ifp)
        ifp.close()

    def test_different_keys(self):
        data = '{"different_key": "whatever"}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    def test_descriptors(self):
        for key, obj in self.valid_schema_desc.descriptors.items():
            name = self.valid_schema_desc.desc[key]["type"]
            self.assertEqual(obj.__class__.__name__, name.capitalize())
            self.assertIn('generate', dir(obj))
            self.assertIn('validate', dir(obj))

    def test_invalid_descriptor(self):
        ifp = open(os.path.join(settings["cwd"], "tests/descs/not_exists_descriptor.json"), "r")
        self.assertRaises(NotFoundDescriptor, DataSchemaDescriptor, ifp)
        ifp.close()
