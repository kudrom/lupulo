import os.path

from twisted.trial import unittest
from mock import patch, MagicMock

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

    def test_descriptors_complete(self):
        for key, obj in self.valid_schema_desc.descriptors.items():
            name = self.valid_schema_desc.desc[key]["type"]
            self.assertEqual(obj.__class__.__name__, name.capitalize())
            self.assertIn('generate', dir(obj))
            self.assertIn('validate', dir(obj))

    @patch('m3dpi_ui.descriptors.number.Number')
    def test_argument_constructors(self, typeMocked):
        ifp = open(os.path.join(settings["cwd"], "tests/descs/argument_constructors.json"), "r")
        dsd = DataSchemaDescriptor(ifp)
        self.assertEqual(typeMocked.called, True)
        typeMocked.assert_called_with(arg0=u'argument0', arg1=u'argument1', type=u'number')

    def test_invalid_descriptor(self):
        ifp = open(os.path.join(settings["cwd"], "tests/descs/not_exists_descriptor.json"), "r")
        self.assertRaises(NotFoundDescriptor, DataSchemaDescriptor, ifp)
        ifp.close()

    def test_validate_different_keys(self):
        data = '{"different_key": "whatever"}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    def test_validate_called(self):
        mocked = MagicMock()
        mocked.validate = MagicMock(return_value=True)
        self.valid_schema_desc.descriptors = {'leds': mocked}
        data = '{"leds": {"arg0": "whatever"}}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        self.assertEqual(mocked.validate.called, True)
        mocked.validate.assert_called_with({"arg0": "whatever"})
