import os.path
import imp

from twisted.web import resource, server, script
from twisted.web.static import File

from jinja2 import Environment, FileSystemLoader

from settings import settings


class LupuloResource(resource.Resource):
    """
        Abstract twisted resource which is inherited by every path
        served by the web server.
    """
    def __init__(self):
        resource.Resource.__init__(self)
        directories = [settings['templates_dir'], settings['lupulo_templates_dir']]
        loader = FileSystemLoader(directories)
        options = {"auto_reload": True, "autoescape": True}
        self.environment = Environment(loader=loader, **options)

    def get_template(self, path):
        return LupuloTemplate(self.environment.get_template(path))

    def getChild(self, name, request):
        """
            Called by twisted to resolve a url.
        """
        if name == '':
            return self
        return resource.Resource.getChild(self, name, request)


class LupuloTemplate(object):
    def __init__(self, template):
        self.template = template

    def render(self):
        utext = self.template.render()
        text = utext.encode('ascii', 'ignore')
        return text


class Root(LupuloResource):
    def __init__(self):
        LupuloResource.__init__(self)
        self.template = self.get_template('index.html')

    def render_GET(self, request):
        return self.template.render()


def connect_user_urls(root):
    try:
        urls = imp.load_source('urls', os.path.join(settings['cwd'], "urls.py"))
    except IOError:
        log.msg("[!] There's no urls.py module valid in the project directory.")
        sys.exit(-1)

    for path, Resource in urls.urlpatterns:
        root.putChild(path, Resource())

def get_website(sse_resource):
    """
        Return the Site for the web server.
    """
    root = Root()
    connect_user_urls(root)

    # If the user has overwritten some urls of the lupulo namespace, they will
    # be overwritten here again
    root.putChild('subscribe', sse_resource)
    #root.putChild('debug', Debug())

    # Serve the static directory for css/js/image files of lupulo
    lupulo_static = File(os.path.join(settings["lupulo_cwd"], 'static'))
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
