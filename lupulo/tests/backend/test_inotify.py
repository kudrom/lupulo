# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

import os.path
import shutil

from twisted.trial import unittest
from twisted.internet.defer import Deferred

from lupulo.settings import settings
from lupulo.inotify_observer import INotifyObserver


class MockInotify(INotifyObserver):
    def __init__(self, d, fp):
        super(MockInotify, self).__init__(fp)
        self.d = d

    def inotify_callback(self, jdata):
        self.d.callback(True)


class TestsInotify(unittest.TestCase):
    def setUp(self):
        self.timeout = 2
        self.old_inotify = settings['activate_inotify']
        settings['activate_inotify'] = True
        cwd = settings["lupulo_cwd"]
        self.path = os.path.join(cwd, 'tests/backend/inotify.txt')
        self.fp = open(self.path, 'w+', 0)
        self.fp.write("you should exist")
        self.d = Deferred()
        self.mock = MockInotify(self.d, self.fp)

    def tearDown(self):
        settings['activate_inotify'] = self.old_inotify
        self.mock.notifier.stopReading()
        self.fp.close()
        os.remove(self.path)

    def test_move(self):
        def clean(_):
            fp.close()
        self.d.addCallback(clean)

        path2 = os.path.join(os.path.dirname(self.path), 'inotify2.txt')
        fp = open(path2, 'w+', 0)

        shutil.move(path2, self.path)

        return self.mock.setup_done

    def test_copy(self):
        def clean(_):
            fp.close()
        self.d.addCallback(clean)

        path2 = os.path.join(os.path.dirname(self.path), 'inotify2.txt')
        fp = open(path2, 'w+', 0)

        shutil.copyfile(path2, self.path)

        return self.d

    def test_overwrite(self):
        self.fp.write('testing')
        self.fp.close()
        return self.d

    def test_not_changes(self):
        def callback(_):
            assert(False)
        self.mock.register_inotify_callback(callback)

        self.fp.write('testing')
        self.fp.close()

        return self.d

    def test_callbacks(self):
        d = Deferred()

        def there_are_changes(jdata):
            jdata['yeah'] = [1]
        self.mock.inotify_callback = there_are_changes

        def callback(_):
            d.callback(True)
        self.mock.register_inotify_callback(callback)

        self.fp.write('testing')
        self.fp.close()

        return d
