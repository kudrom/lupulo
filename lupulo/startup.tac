# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

import os
import sys

from lupulo.settings import settings as lupulo_settings
lupulo_settings['cwd'] = os.environ['LUPULO_PROJECT_DIR']
from settings import settings

from twisted.application import service, internet
from twisted.python import log
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

from lupulo.sse_resource import SSEResource
from lupulo.root import get_website
from lupulo.listeners_manager import listeners_manager


# Bind the application and create a multi service that will be the
# father of all the services below
application = service.Application("m3pdi_ui")
multi = service.MultiService()
multi.setServiceParent(application)

# Setup logging
logfile = DailyLogFile(settings["log_file"], "/var/log/lupulo/")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

# Log to stdout too
if settings["redirect_stdout"]:
    log.FileLogObserver(sys.stdout).start()

# Create the web server and attach it to multi
sse_resource = SSEResource()
site = get_website(sse_resource)
tcp_server = internet.TCPServer(settings["web_server_port"], site)
tcp_server.setServiceParent(multi)

# Create the serial listener and attach it to multi
listeners_manager.connect_listener(multi, sse_resource)
