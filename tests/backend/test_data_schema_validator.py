import os.path

from twisted.trial import unittest
from mock import patch, MagicMock

from lupulo.data_schema_manager import DataSchemaManager
from lupulo.settings import settings


class TestDataSchemaValidations(unittest.TestCase):
    def setUp(self):
        self.cwd = "/".join(settings["lupulo_cwd"].split("/")[:-1])
        test = "tests/backend/data_schemas/complete.json"
        self.fp = open(os.path.join(self.cwd, test), "r")
        self.old_inotify = settings['activate_inotify']
        settings['activate_inotify'] = False
        self.valid_schema_desc = DataSchemaManager(self.fp)

    def tearDown(self):
        settings['activate_inotify'] = self.old_inotify
        self.fp.close()

    def test_validation_number(self):
        data = '{"rotation": 180, "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        data = '{"rotation": 400, "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"direction": 180, "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    def test_validation_enum(self):
        test = "tests/backend/data_schemas/enum.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        dsd = DataSchemaManager(ifp)
        data = '{"interesting_name": 1, "id": 1}'
        self.assertEqual(dsd.validate(data), True)
        data = '{"interesting_name": 2, "id": 1}'
        self.assertEqual(dsd.validate(data), True)
        data = '{"interesting_name": 3, "id": 1}'
        self.assertEqual(dsd.validate(data), True)
        data = '{"interesting_name": 4, "id": 1}'
        self.assertEqual(dsd.validate(data), False)

    def test_validation_list(self):
        data = """
            {
             "id": 1,
             "leds": ["on", "off", "null", "on",
                      "null", "off", "null", "on"]
            }
        """
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        data = """
            {
             "id": 1,
             "leds": ["on", "off", "null", "on",
                      "null", "off", "null", "on",
                      "off"]
            }
        """
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = """
            {
             "id": 1,
             "leds": ["shit", "off", "null", "on",
                      "null", "off", "null", "on"]
            }
        """
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"leds": ["off"], "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    @patch('lupulo.descriptors.enum.Enum')
    def test_validation_list_calls(self, EnumMock):
        test = "tests/backend/data_schemas/list.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        dsd = DataSchemaManager(ifp)
        EnumMock.assert_called_once_with(values=["on", "off", "null"])
        data = '{"leds": ["on", "off", "null"], "id": 1}'
        validate = MagicMock(return_value=True)
        dsd.descriptors["leds"].delegate.validate = validate
        self.assertEqual(dsd.validate(data), True)
        self.assertEqual(validate.call_count, 3)

    def test_validation_dict(self):
        data = '{"motor": {"speed": 1.45, "turn_radius": 2.32}, "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), True)
        data = '{"motor": {"turn_radius": 2.32}, "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = """
            {
             "id": 1,
             "motor": {"speed": 1.45,
                       "turn_radius": 2.32,
                       "something": 5.55}
            }
        """
        self.assertEqual(self.valid_schema_desc.validate(data), False)
        data = '{"motor": {"speed": 1000, "turn_radius": 2.32}, "id": 1}'
        self.assertEqual(self.valid_schema_desc.validate(data), False)

    @patch('lupulo.descriptors.enum.Enum')
    @patch('lupulo.descriptors.number.Number')
    def test_validation_dict_calls(self, NumberMock, EnumMock):
        test = "tests/backend/data_schemas/dict.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        dsd = DataSchemaManager(ifp)
        EnumMock.assert_called_once_with(values=[0, 3], type="enum")
        NumberMock.assert_called_once_with(range=[0, 5], type="number")
        data = '{"motor": {"speed": 4, "turn_radius": 3}, "id": 1}'
        v_enum = MagicMock(return_value=True)
        v_number = MagicMock(return_value=True)
        dsd.descriptors["motor"].delegates["speed"].validate = v_number
        dsd.descriptors["motor"].delegates["turn_radius"].validate = v_enum
        self.assertEqual(dsd.validate(data), True)
        v_enum.assert_called_once_with(3)
        v_number.assert_called_once_with(4)

    @patch('lupulo.descriptors.number.Number')
    def test_validaton_nested_list_dict(self, MockNumber):
        mock_validate = MagicMock(return_value=True)
        MockNumber().validate = mock_validate
        test = "tests/backend/data_schemas/list_dict.json"
        ifp = open(os.path.join(self.cwd, test), "r")
        dsd = DataSchemaManager(ifp)
        data = """
            {
             "id": 1,
             "motor": [{"speed": 4, "turn_radius": 3},
                       {"speed": 3, "turn_radius": 2}]
            }
        """
        dsd.validate(data)
        self.assertEqual(mock_validate.called, True)
