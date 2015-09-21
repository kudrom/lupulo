import os.path

from twisted.web import resource, server
from twisted.web.template import Element, renderer, XMLFile, flatten
from twisted.web.static import File
from twisted.python.filepath import FilePath

from settings import settings
from sse_resource import SSE_Resource


class Root(resource.Resource):
    def getChild(self, name, request):
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        d = flatten(request, RootElement(), request.write)
        d.addCallback(lambda _, x: x.finish(), request)
        return server.NOT_DONE_YET

class RootElement(Element):
    loader = XMLFile(FilePath(os.path.join(settings["templates_dir"], "index.html")))




def get_website(sse_resource):
    root = Root()
    static = File('static')
    root.putChild('subscribe', sse_resource)
    root.putChild('static', static)
    return server.Site(root)
