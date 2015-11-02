from twisted.internet.inotify import INotify
from twisted.python.filepath import FilePath

from lupulo.settings import settings


class INotifyObserver(object):
    def __init__(self, fp):
        self.fp = fp
        if settings["activate_inotify"]:
            self.setup_inotify()
        self.inotify_callbacks = []

    def setup_inotify(self):
        self.notifier = INotify()
        self.notifier.startReading()
        filepath = FilePath(self.fp.name)
        self.notifier.watch(filepath, callbacks=[self.inotify])

    def register_inotify_callback(self, callback):
        self.inotify_callbacks.append(callback)
