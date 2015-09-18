from twisted.web import resource


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
