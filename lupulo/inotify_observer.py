from twisted.internet.inotify import INotify, humanReadableMask
from twisted.python.filepath import FilePath
from twisted.python import log
from twisted.internet.defer import Deferred

from lupulo.settings import settings


class INotifyObserver(object):
    def __init__(self, fp):
        self.fp = fp
        self.setup_done = Deferred()
        if settings["activate_inotify"]:
            self.setup_inotify()
        self.inotify_callbacks = []

    def setup_inotify(self):
        """
            Setup the INotifier watcher.
        """
        self.notifier = INotify()
        self.notifier.startReading()
        filepath = FilePath(self.fp.name)
        self.notifier.watch(filepath, callbacks=[self.inotify])

        # The setup_done is used mainly in testing
        self.setup_done.callback(True)
        self.setup_done = Deferred()


    def register_inotify_callback(self, callback):
        self.inotify_callbacks.append(callback)

    def inotify_callback(self, jdata):
        """
            Must be overwritten by a child.
        """
        raise NotImplementedError

    def inotify(self, ignored, filepath, mask):
        """
            Callback for the INotify. It should call the sse resource with the
            changed layouts in the layout file if there are changes in the
            layout file.
            It calls the inotify_callback method first which must be overwritten
            by its children.
        """
        hmask = humanReadableMask(mask)

        # Some editors move the file triggering several events in inotify. All
        # of them change some attribute of the file, so if that event happens,
        # see if there are changes and alert the sse resource in that case.
        if 'attrib' in hmask or 'modify' in hmask:
            self.fp.close()
            self.fp = open(self.fp.name, 'r')
            self.fp.seek(0)

            jdata = {}
            self.inotify_callback(jdata)

            changes = 0
            for _, l in jdata.items():
                changes += len(l)

            if changes > 0:
                for callback in self.inotify_callbacks:
                    callback(jdata)
                log.msg("Change in %s" % self.fp.name)

        # Some editors move the file and inotify lose track of the file, so the
        # notifier must be restarted when some attribute changed is received.
        if 'attrib' in hmask:
            self.notifier.stopReading()
            self.setup_inotify()
