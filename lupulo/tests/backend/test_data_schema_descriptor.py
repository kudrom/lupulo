import os.path

from twisted.trial import unittest
from mock import patch, MagicMock

from lupulo.data_schema_manager import DataSchemaManager
from lupulo.settings import settings
from lupulo.exceptions import NotFoundDescriptor, RequirementViolated


class TestsSchemaDescriptor(unittest.TestCase):
    def setUp(self):
        self.cwd = settings["lupulo_cwd"]
        schema = "tests/backend/data_schemas/complete.json"
        self.fp = open(os.path.join(self.cwd, schema), "r")
        self.old_inotify = settings['activate_inotify']
        settings['activate_inotify'] = False
        self.valid_schema_desc = DataSchemaManager(self.fp)

    def tearDown(self):
        settings['activate_inotify'] = self.old_inotify
        self.fp.close()

    def test_invalid_file(self):
        test = "tests/backend/data_schemas/invalid_syntax.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        self.assertRaises(ValueError, DataSchemaManager, ifp)
        ifp.close()

    def test_descriptors_complete(self):
        for key, obj in self.valid_schema_desc.descriptors.items():
            name = self.valid_schema_desc.desc[key]["type"]
            self.assertEqual(obj.__class__.__name__, name.capitalize())
            self.assertIn('generate', dir(obj))
            self.assertIn('validate', dir(obj))

    @patch('lupulo.descriptors.number.Number')
    def test_argument_constructors(self, typeMocked):
        test = "tests/backend/data_schemas/argument_constructors.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        DataSchemaManager(ifp)
        self.assertEqual(typeMocked.called, True)
        typeMocked.assert_called_with(arg0=u'argument0',
                                      arg1=u'argument1',
                                      type=u'number')

    def test_invalid_descriptor(self):
        test = "tests/backend/data_schemas/not_exists_descriptor.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        self.assertRaises(NotFoundDescriptor, DataSchemaManager, ifp)
        ifp.close()

    def test_requirement_violated(self):
        test = "tests/backend/data_schemas/requirements.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        self.assertRaises(RequirementViolated, DataSchemaManager, ifp)

    def test_validate_different_keys(self):
        data = '{"different_key": "whatever", "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    def test_validate_no_id(self):
        data = '{"battery": 62}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    def test_validate_called(self):
        mocked = MagicMock()
        mocked.validate = MagicMock(return_value=True)
        self.valid_schema_desc.descriptors = {'leds': mocked}
        data = '{"leds": ["on", "off", "on"], "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        self.assertEqual(mocked.validate.called, True)
        mocked.validate.assert_called_with(["on", "off", "on"])

    @patch('lupulo.descriptors.dict.Dict')
    def test_construction_nested_list_dict(self, MockedDict):
        test = "tests/backend/data_schemas/list_dict.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        DataSchemaManager(ifp)
        MockedDict.assert_called_once_with(keys=["speed", "turn_radius"],
                                           speed_type="number",
                                           speed_range=[0, 5],
                                           turn_radius_type="number",
                                           turn_radius_range=[0, 3])

    def test_attributes_nested_list_dict(self):
        test = "tests/backend/data_schemas/list_dict.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        dsd = DataSchemaManager(ifp)
        motor = dsd.descriptors["motor"]
        self.assertEqual(motor.delegate.__class__.__name__, "Dict")
        self.assertEqual(len(motor.delegate.delegates), 2)
        self.assertEqual(set(motor.delegate.delegates.keys()),
                         set(["speed", "turn_radius"]))
        self.assertEqual(motor.delegate.delegates["speed"].__class__.__name__,
                         "Number")
