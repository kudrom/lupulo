# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

import os.path

from twisted.trial import unittest
from mock import MagicMock

from lupulo.layout_manager import LayoutManager
from lupulo.settings import settings


class TestsLayout(unittest.TestCase):
    def setUp(self):
        self.old_value = settings['activate_inotify']
        settings['activate_inotify'] = False

        self.cwd = settings["lupulo_cwd"]
        test = "tests/backend/layouts/complete.json"
        self.fp = open(os.path.join(self.cwd, test), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["distances",
                                              "something_else"])

        self.layout_manager = LayoutManager(self.fp, schema_manager)
        self.raw = self.layout_manager.raw

        self.contexts = self.layout_manager.contexts
        self.contexts["global"] = self.raw["global"]
        self.contexts["distances"] = self.raw["distances"]

    def tearDown(self):
        self.fp.close()
        settings['activate_inotify'] = self.old_value

    def invalid(self, filepath):
        layout_path = "tests/backend/layouts/" + filepath
        ifp = open(os.path.join(self.cwd, layout_path), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["something"])
        self.layout_manager = LayoutManager(ifp, schema_manager)
        self.layout_manager.compile()
        self.assertEqual(len(self.layout_manager.layouts), 0)
        ifp.close()

    def test_invalid_event(self):
        self.invalid("invalid_event.json")

    def test_invalid_size(self):
        self.invalid("invalid_size.json")

    def test_invalid_accessors(self):
        self.invalid("invalid_accessors.json")

    def test_default_accessor(self):
        layout_path = "tests/backend/layouts/" + "default_accessor.json"
        ifp = open(os.path.join(self.cwd, layout_path), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["something"])
        self.layout_manager = LayoutManager(ifp, schema_manager)
        self.layout_manager.compile()
        self.assertEqual(len(self.layout_manager.layouts), 1)
        accessor = self.layout_manager.layouts['battery']["accessors"][0]
        self.assertEqual(accessor["event"], "something")
        ifp.close()

    def test_accessor_with_event(self):
        layout_path = "tests/backend/layouts/" + "accessor_with_event.json"
        ifp = open(os.path.join(self.cwd, layout_path), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["something"])
        self.layout_manager = LayoutManager(ifp, schema_manager)
        self.layout_manager.compile()
        self.assertEqual(len(self.layout_manager.layouts), 1)
        ifp.close()

    def test_accessor_chaining_invalid(self):
        self.invalid("chaining_invalid.json")

    def test_accessor_chaining_valid(self):
        layout_path = "tests/backend/layouts/" + "chaining_valid.json"
        ifp = open(os.path.join(self.cwd, layout_path), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["something"])
        self.layout_manager = LayoutManager(ifp, schema_manager)
        self.layout_manager.compile()
        self.assertEqual(len(self.layout_manager.layouts), 1)
        ifp.close()

    def test_accessor_object(self):
        layout_path = "tests/backend/layouts/" + "accessor_object.json"
        ifp = open(os.path.join(self.cwd, layout_path), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["something"])
        self.layout_manager = LayoutManager(ifp, schema_manager)
        self.layout_manager.compile()
        self.assertEqual(len(self.layout_manager.layouts), 1)
        accessor = self.layout_manager.layouts['battery']['accessors']
        self.assertEqual(accessor['battery']['event'], 'something')
        ifp.close()

    def test_missing_attributes(self):
        self.invalid("missing_attributes.json")

    def test_one_level_inheritance(self):
        layout = self.raw["distances"]
        obj = self.layout_manager.inherit(layout)
        attributes = ["anchor", "overwritten", "abstract",
                      "parent", "range", "seconds", "size", "margin"]
        self.assertEqual(set(obj.keys()), set(attributes))

    def test_two_levels_inheritance(self):
        layout = self.raw["distances-center"]
        obj = self.layout_manager.inherit(layout)
        attributes = ["anchor", "overwritten", "parent", "range",
                      "seconds", "event_names", "type", "size", "margin"]
        self.assertEqual(set(obj.keys()), set(attributes))

    def test_overwritten(self):
        layout = self.raw["overwritten"]
        obj = self.layout_manager.inherit(layout)
        self.assertEqual(obj["overwritten"], True)

    def test_invalid_parent(self):
        self.invalid("invalid_parent.json")

    def test_bug_events_accessors(self):
        layout_path = "tests/backend/layouts/" + "bug_events_accessor.json"
        ifp = open(os.path.join(self.cwd, layout_path), "r")
        schema_manager = MagicMock()
        schema_manager.get_events = MagicMock(return_value=["battery", "date"])
        self.layout_manager = LayoutManager(ifp, schema_manager)
        self.layout_manager.compile()
        self.assertEqual(set(self.layout_manager.layouts.keys()),
                         set(['battery-widget', 'device_time']))
        self.assertEqual(self.layout_manager.layouts['battery-widget']['accessors'][0]['event'], 'battery')

    def test_compile_correct(self):
        self.layout_manager.compile()
        layouts = self.layout_manager.layouts
        self.assertEqual(set(layouts.keys()),
                         set(["simple", "distances-center", "overwritten"]))
        self.assertEqual(set(layouts["simple"].keys()),
                         set(["name", "type", "event_names", "anchor",
                              "size", "margin"]))
        self.assertEqual(layouts["simple"]["type"], 1)
        self.assertEqual(layouts["simple"]["event_names"], ["something_else"])
        attributes = ["anchor", "name", "type", "event_names",
                      "range", "overwritten", "seconds", "size", "margin"]
        self.assertEqual(set(layouts["distances-center"].keys()),
                         set(attributes))
        self.assertEqual(layouts["distances-center"]["overwritten"], False)
        self.assertEqual(set(layouts["overwritten"].keys()),
                         set(attributes))
        self.assertEqual(layouts["overwritten"]["overwritten"], True)

    def difference(self, filepath, result):
        self.layout_manager.compile()

        layout_path = "tests/backend/layouts/" + filepath
        ifp = open(os.path.join(self.cwd, layout_path), "r")

        self.layout_manager.fp = ifp
        jdata = {}
        self.layout_manager.inotify_callback(jdata)
        self.assertEqual(jdata, result)

        ifp.close()

    def test_inotify_difference_added(self):
        jdata = {}
        jdata['removed'] = []
        jdata['changed'] = {}
        jdata['added'] = {
            'distances2': {
                'overwritten': False,
                'name': 'distances2',
                'seconds': 100,
                'range': [0, 4],
                'type': 'multiple_line',
                'anchor': 0,
                'event_names': ['distances'],
                'size': {'width': 800, 'height': 600},
                "margin": {"top": 0, "bottom": 0, "right": 0, "left": 0}
            }
        }
        self.difference('difference_added.json', jdata)

    def test_inotify_difference_removed(self):
        jdata = {}
        jdata['removed'] = ['distances-center']
        jdata['changed'] = {}
        jdata['added'] = {}
        self.difference('difference_removed.json', jdata)

    def test_inotify_difference_changed(self):
        jdata = {}
        jdata['removed'] = []
        jdata['added'] = {}
        jdata['changed'] = {
            'distances-center': {
                'overwritten': False,
                'name': 'distances-center',
                'seconds': 100,
                'range': [0, 4],
                'type': 'awesomeness',
                'anchor': 0,
                'event_names': ['distances'],
                'size': {'width': 800, 'height': 600},
                "margin": {"top": 0, "bottom": 0, "right": 0, "left": 0}
            }
        }
        self.difference('difference_changed.json', jdata)

    def test_inotify_not_difference(self):
        self.layout_manager.compile()
        jdata = {}
        self.layout_manager.inotify_callback(jdata)
        self.assertEqual(jdata, {'added': {}, 'changed': {}, 'removed': []})
