from twisted.web import server, resource


class Root(resource.Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        return r"""
        <html>
            <head>
                <script language="JavaScript">
                        eventSource = new EventSource("http://localhost:8080/subscribe");
                        eventSource.onmessage = function(event) {
                            element = document.getElementById("event-data");
                            element.innerHTML = event.data;
                        };
                    </script>
            </head>
            <body>
                <h1> m3dpi demo</h1>
                <h3> Event data: </h3>
                <p id="event-data"></p>
            </body>
        </html>
        """


class SSE_Resource(resource.Resource):
    isLeaf = True

    def __init__(self):
        self.subscribers = set()

    def render_GET(self, request):
        request.setHeader('Content-Type', 'text/event-stream; charset=utf-8')
        request.setResponseCode(200)
        self.subscribers.add(request)
        d = request.notifyFinish()
        d.addBoth(self.removeSubscriber)
        request.write("")
        return server.NOT_DONE_YET

    def publish(self, data):
        for subscriber in self.subscribers:
            for line in data:
                subscriber.write("data: %s\r\n" % line)
            subscriber.write("\r\n")

    def removeSubscriber(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)
