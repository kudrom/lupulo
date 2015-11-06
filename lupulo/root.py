import os.path

from twisted.web import resource, server, script
from twisted.web.template import Element, XMLFile, flatten
from twisted.web.static import File
from twisted.python.filepath import FilePath

from settings import settings


class AbstractResource(resource.Resource):
    """
        Abstract twisted resource which is inherited by every path
        served by the web server.
    """
    def __init__(self):
        resource.Resource.__init__(self)

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
    def __init__(self, page="", directory=""):
        Element.__init__(self)
        if directory == "":
            directory = settings["templates_dir"]
        filepath = os.path.join(directory, page)
        self.loader = XMLFile(FilePath(filepath))


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
        directory = settings['lupulo_templates_dir']
        AbstractElement.__init__(self, "index.html", directory)


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
        directory = settings['lupulo_templates_dir']
        AbstractElement.__init__(self, "debug.html", directory)


def get_website(sse_resource):
    """
        Return the Site for the web server.
    """
    root = Root()
    root.putChild('subscribe', sse_resource)
    root.putChild('debug', Debug())

    # Serve the static directory for css/js/image files of lupulo
    lupulo_static = File(os.path.join(settings["lupulo_cwd"], 'defaults/static'))
    root.putChild('lupulo_static', lupulo_static)

    # Serve the static directory for css/js/image files of the project
    static = File(os.path.join(settings["cwd"], 'static'))
    root.putChild('static', static)

    command = File(os.path.join(settings["cwd"], 'rest'))
    command.ignoreExt('.rpy')
    command.processors = {'.rpy': script.ResourceScript}
    root.putChild('command', command)

    if settings['debug_lupulo']:
        testing = File(os.path.join(settings["cwd"], 'tests/frontend'))
        root.putChild('testing', testing)

    return server.Site(root)
