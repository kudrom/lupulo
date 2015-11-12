import os
import os.path
import shutil

from twisted.trial import unittest
from mock import MagicMock

from lupulo.settings import settings
from lupulo.listeners_manager import connect_listener, get_listener_name
from lupulo.exceptions import NotListenerFound

missing_listener = """
class MissingListener(object):
    def __init__(self, sse_resource):
        self.sse_resource = sse_resource
"""

awesome_listener = """
class AwesomeListener(object):
    def __init__(self, sse_resource):
        self.sse_resource = sse_resource

    def setServiceParent(self, parent):
        self.parent = parent
"""


class TestsListenerManager(unittest.TestCase):
    def setUp(self):
        self.old_settings = settings
        self.mock_sse_resource = MagicMock()
        self.mock_parent = MagicMock()

    def tearDown(self):
        settings = self.old_settings
        if os.path.exists('../listeners'):
            shutil.rmtree('../listeners')

    def create_listener(self, name, text):
        settings['listener'] = name
        os.mkdir('../listeners')

        path = os.path.join('../listeners', name + '_listener.py')
        with open(path, 'w+') as fp:
            fp.write(text)

        fp = open('../listeners/__init__.py', 'w+')
        fp.close()

    def test_missing_module(self):
        settings['listener'] = 'crap'
        self.assertRaises(NotListenerFound, connect_listener, self.mock_parent,
                          self. mock_sse_resource)

    def test_missing_listener(self):
        self.create_listener('incredible', missing_listener)
        self.assertRaises(NotListenerFound, connect_listener, 'parent', 'sse')

    def test_listener_constructed(self):
        self.create_listener('awesome', awesome_listener)
        listener = connect_listener('parent', 'sse')
        self.assertEqual(listener.sse_resource, 'sse')
        self.assertEqual(listener.parent, 'parent')

    def test_underscore(self):
        name = get_listener_name("something_weird")
        self.assertEqual(name, "SomethingWeirdListener")

    def test_double_underscore(self):
        name = get_listener_name("something__weird")
        self.assertEqual(name, "SomethingWeirdListener")

    def test_no_underscore(self):
        name = get_listener_name("somethingweird")
        self.assertEqual(name, "SomethingweirdListener")
