import os.path

from twisted.web import resource, server
from twisted.web.template import Element, renderer, XMLFile, flatten
from twisted.web.static import File
from twisted.python.filepath import FilePath

from m3dpi_ui.settings import settings


class Root(resource.Resource):
    """
        Root resource of the web server.
    """
    def getChild(self, name, request):
        """
            Called by twisted to resolve a url.
        """
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)

    def render_GET(self, request):
        """
            Called by twisted to render a GET http request.
        """
        d = flatten(request, RootElement(), request.write)
        d.addCallback(lambda _, x: x.finish(), request)
        return server.NOT_DONE_YET

class RootElement(Element):
    """
        Called by Root to render the template.
    """
    loader = XMLFile(FilePath(os.path.join(settings["templates_dir"], "index.html")))




def get_website(sse_resource):
    """
        Return the Site for the web server.
    """
    root = Root()
    root.putChild('subscribe', sse_resource)
    # Serve the static directory for css/js/image files
    static = File(os.path.join(settings["cwd"], 'static'))
    root.putChild('static', static)
    return server.Site(root)
