import os.path

from twisted.trial import unittest
from mock import patch, MagicMock

from m3dpi_ui.layout_manager import LayoutManager
from m3dpi_ui.settings import settings


class TestsSchemaDescriptor(unittest.TestCase):
    def setUp(self):
        self.fp = open(os.path.join(settings["cwd"], "tests/layouts/complete.json"), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["distances", "something_else"])
        self.layout_manager = LayoutManager(self.fp, schema_manager)

    def tearDown(self):
        self.fp.close()

    def invalid(self, filepath):
        ifp = open(os.path.join(settings["cwd"], "tests/layouts/" + filepath), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["something"])
        self.layout_manager = LayoutManager(ifp, schema_manager)
        self.layout_manager.compile()
        self.assertEqual(len(self.layout_manager.layouts), 0)
        ifp.close()

    def test_invalid_event(self):
        self.invalid("invalid_event.json")

    def test_missing_attributes(self):
        self.invalid("missing_attributes.json")

    def test_one_level_inheritance(self):
        layout = self.layout_manager.raw["distances"]
        self.layout_manager.contexts["global"] = self.layout_manager.raw["global"]
        obj = self.layout_manager.inherit(layout)
        self.assertEqual(set(obj.keys()), set(["anchor", "overwritten", "abstract", "parent", "range", "seconds"]))

    def test_two_levels_inheritance(self):
        layout = self.layout_manager.raw["distances-center"]
        self.layout_manager.contexts["global"] = self.layout_manager.raw["global"]
        self.layout_manager.contexts["distances"] = self.layout_manager.raw["distances"]
        obj = self.layout_manager.inherit(layout)
        self.assertEqual(set(obj.keys()), set(["anchor", "overwritten", "parent", "range", "seconds", "event_name", "type"]))

    def test_overwritten(self):
        layout = self.layout_manager.raw["overwritten"]
        self.layout_manager.contexts["global"] = self.layout_manager.raw["global"]
        self.layout_manager.contexts["distances"] = self.layout_manager.raw["distances"]
        obj = self.layout_manager.inherit(layout)
        self.assertEqual(set(obj.keys()), set(["anchor", "overwritten", "parent", "range", "seconds", "event_name" , "type"]))
        self.assertEqual(obj["overwritten"], True)

    def test_invalid_parent(self):
        self.invalid("invalid_parent.json")

    def test_compile_correct(self):
        self.layout_manager.compile()
        layouts = self.layout_manager.layouts
        self.assertEqual(set(layouts.keys()), set(["simple", "distances-center", "overwritten"]))
        self.assertEqual(set(layouts["simple"].keys()), set(["name", "type", "event_name", "anchor"]))
        self.assertEqual(layouts["simple"]["type"], 1)
        self.assertEqual(layouts["simple"]["event_name"], "something_else")
        self.assertEqual(set(layouts["distances-center"].keys()), set(["anchor", "name", "type", "event_name", "range", "overwritten", "seconds"]))
        self.assertEqual(layouts["distances-center"]["overwritten"], False)
        self.assertEqual(set(layouts["overwritten"].keys()), set(["anchor", "name", "type", "event_name", "range", "overwritten", "seconds"]))
        self.assertEqual(layouts["overwritten"]["overwritten"], True)
