import os.path

from twisted.web import resource, server
from twisted.web.template import Element, renderer, XMLFile, flatten
from twisted.web.static import File
from twisted.python.filepath import FilePath

from m3dpi_ui.settings import settings


class AbstractResource(resource.Resource):
    """
        Abstract twisted resource which is inherited by every path
        served by the web server.
    """
    def __init__(self):
        resource.Resource.__init__(self)
        self.element_delegate = AbstractElement("")

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
        d = flatten(request, self.element_delegate, request.write)
        d.addCallback(lambda _, x: x.finish(), request)
        return server.NOT_DONE_YET

class AbstractElement(Element):
    """
        Abstract twisted resource which is inherited to render all
        the webpages of the web server.
    """
    def __init__(self, page=""):
        Element.__init__(self)
        self.loader = XMLFile(FilePath(os.path.join(settings["templates_dir"], page)))


class Root(AbstractResource):
    """
        Root resource of the web server.
    """
    def __init__(self):
        AbstractResource.__init__(self)
        self.element_delegate = RootElement()


class RootElement(AbstractElement):
    """
        Called by Root to render the template.
    """
    def __init__(self):
        AbstractElement.__init__(self, "index.html")

class Debug(AbstractResource):
    """
        Debug resource of the web server.
    """
    def __init__(self):
        AbstractResource.__init__(self)
        self.element_delegate = DebugElement()

class DebugElement(AbstractElement):
    """
        Called by Debug to render the template.
    """
    def __init__(self):
        AbstractElement.__init__(self, "debug.html")




def get_website(sse_resource):
    """
        Return the Site for the web server.
    """
    root = Root()
    root.putChild('subscribe', sse_resource)
    root.putChild('debug', Debug())
    # Serve the static directory for css/js/image files
    static = File(os.path.join(settings["cwd"], 'static'))
    root.putChild('static', static)
    return server.Site(root)
