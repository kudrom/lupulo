from twisted.internet import reactor

from lupulo.tests.sse_client.sse_client import SSEClient
from lupulo.settings import settings

URL = 'http://localhost:' + str(settings['web_server_port']) + '/subscribe'


def onmessage(data):
    print 'Got payload with data %s' % data

if __name__ == '__main__':
    """
        Launches the reactor for infinite time, this should be launched in the
        project's main directory with PYTHONPATH='.:$PYTHONPATH'
    """
    client = SSEClient(URL)
    client.addEventListener("id1-battery", onmessage)
    client.connect()
    reactor.run()
