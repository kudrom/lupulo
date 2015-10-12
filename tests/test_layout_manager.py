import os.path

from twisted.trial import unittest
from mock import patch, MagicMock

from m3dpi_ui.layout_manager import LayoutManager
from m3dpi_ui.settings import settings


class TestsSchemaDescriptor(unittest.TestCase):
    def setUp(self):
        self.fp = open(os.path.join(settings["cwd"], "tests/layouts/complete.json"), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["simple", "two", "three"])
        self.layout_manager = LayoutManager(self.fp, schema_manager)

    def tearDown(self):
        self.fp.close()

    def test_wighout_correct_event(self):
        pass

    def test_without_inheritance(self):
        pass

    def test_one_level_inheritance(self):
        pass

    def test_two_levels_inheritance(self):
        pass

    def test_invalid_parent(self):
        pass

    def test_parent_who_is_not_abstract(self):
        pass

    def test_compile_correct(self):
        pass
