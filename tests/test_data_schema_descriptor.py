import os.path
import json

from twisted.trial import unittest
from mock import patch, MagicMock

from m3dpi_ui.data_schema_manager import DataSchemaManager
from m3dpi_ui.settings import settings
from m3dpi_ui.exceptions import NotFoundDescriptor, RequirementViolated


class TestsSchemaDescriptor(unittest.TestCase):
    def setUp(self):
        self.fp = open(os.path.join(settings["cwd"], "tests/data_schemas/complete.json"), "r")
        self.valid_schema_desc = DataSchemaManager(self.fp)

    def tearDown(self):
        self.fp.close()

    def test_invalid_file(self):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/invalid_syntax.json"), "r")
        self.assertRaises(ValueError, DataSchemaManager, ifp)
        ifp.close()

    def test_descriptors_complete(self):
        for key, obj in self.valid_schema_desc.descriptors.items():
            name = self.valid_schema_desc.desc[key]["type"]
            self.assertEqual(obj.__class__.__name__, name.capitalize())
            self.assertIn('generate', dir(obj))
            self.assertIn('validate', dir(obj))

    @patch('m3dpi_ui.descriptors.number.Number')
    def test_argument_constructors(self, typeMocked):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/argument_constructors.json"), "r")
        dsd = DataSchemaManager(ifp)
        self.assertEqual(typeMocked.called, True)
        typeMocked.assert_called_with(arg0=u'argument0', arg1=u'argument1', type=u'number')

    def test_invalid_descriptor(self):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/not_exists_descriptor.json"), "r")
        self.assertRaises(NotFoundDescriptor, DataSchemaManager, ifp)
        ifp.close()

    def test_requirement_violated(self):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/requirements.json"), "r")
        self.assertRaises(RequirementViolated, DataSchemaManager, ifp)

    def test_validate_different_keys(self):
        data = '{"different_key": "whatever"}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    def test_validate_called(self):
        mocked = MagicMock()
        mocked.validate = MagicMock(return_value=True)
        self.valid_schema_desc.descriptors = {'leds': mocked}
        data = '{"leds": ["on", "off", "on"]}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        self.assertEqual(mocked.validate.called, True)
        mocked.validate.assert_called_with(["on", "off", "on"])

    def test_validation_number(self):
        data = '{"rotation": 180}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        data = '{"rotation": 400}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"direction": 180}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    def test_validation_enum(self):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/enum.json"), "r")
        dsd = DataSchemaManager(ifp)
        data = '{"interesting_name": 1}'
        self.assertEqual(dsd.validate(data), True)
        data = '{"interesting_name": 2}'
        self.assertEqual(dsd.validate(data), True)
        data = '{"interesting_name": 3}'
        self.assertEqual(dsd.validate(data), True)
        data = '{"interesting_name": 4}'
        self.assertEqual(dsd.validate(data), False)

    def test_validation_list(self):
        data = '{"leds": ["on", "off", "null", "on", "null", "off", "null", "on"]}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        data = '{"leds": ["on", "off", "null", "on", "null", "off", "null", "on", "off"]}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"leds": ["shit", "off", "null", "on", "null", "off", "null", "on"]}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"leds": ["off"]}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    @patch('m3dpi_ui.descriptors.enum.Enum')
    def test_validation_list_calls(self, EnumMock):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/list.json"), "r")
        dsd = DataSchemaManager(ifp)
        EnumMock.assert_called_once_with(values=["on", "off", "null"])
        data = '{"leds": ["on", "off", "null"]}'
        validate = MagicMock(return_value=True)
        dsd.descriptors["leds"].delegate.validate = validate
        self.assertEqual(dsd.validate(data), True)
        self.assertEqual(validate.call_count, 3)

    def test_validation_dict(self):
        data = '{"motor": {"speed": 1.45, "turn_radius": 2.32}}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        data = '{"motor": {"turn_radius": 2.32}}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"motor": {"speed": 1.45, "turn_radius": 2.32, "something": 5.55}}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"motor": {"speed": 1000, "turn_radius": 2.32}}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    @patch('m3dpi_ui.descriptors.enum.Enum')
    @patch('m3dpi_ui.descriptors.number.Number')
    def test_validation_dict_calls(self, NumberMock, EnumMock):
        ifp = open(os.path.join(settings["cwd"], "tests/data_schemas/dict.json"), "r")
        dsd = DataSchemaManager(ifp)
        EnumMock.assert_called_once_with(values=[0, 3], type="enum")
        NumberMock.assert_called_once_with(range=[0, 5], type="number")
        data = '{"motor": {"speed": 4, "turn_radius": 3}}'
        validate_enum = MagicMock(return_value=True)
        validate_number = MagicMock(return_value=True)
        dsd.descriptors["motor"].delegates["speed"].validate = validate_number
        dsd.descriptors["motor"].delegates["turn_radius"].validate = validate_enum
        self.assertEqual(dsd.validate(data), True)
        validate_enum.assert_called_once_with(3)
        validate_number.assert_called_once_with(4)

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
