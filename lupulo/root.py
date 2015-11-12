import os.path
import imp
import sys

from twisted.web import resource, server, script
from twisted.web.static import File
from twisted.python import log

from jinja2 import Environment, FileSystemLoader

from settings import settings


class LupuloResource(resource.Resource):
    """
        Abstract twisted resource which is inherited by every path
        served by the web server.
    """
    def __init__(self, next_resources):
        resource.Resource.__init__(self)
        self.next_resources = next_resources
        directories = []
        directories.append(settings['templates_dir'])
        directories.append(settings['lupulo_templates_dir'])
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
        else:
            if name in self.next_resources:
                return self.next_resources[name]
        return resource.Resource.getChild(self, name, request)


class LupuloTemplate(object):
    """
        Adapter around a jinja2 template which will render the template in an
        asynchronous way.
    """
    def __init__(self, template):
        self.template = template

    def render(self):
        utext = self.template.render()
        text = utext.encode('ascii', 'ignore')
        return text


class Root(LupuloResource):
    """
        Root resource for the index.html template of the project.
    """
    def __init__(self, *args):
        LupuloResource.__init__(self, *args)
        self.template = self.get_template('index.html')

    def render_GET(self, request):
        return self.template.render()


def connect_user_urls(root):
    """
        Reads the urls defined by the user and creates all necessary resources.
    """
    try:
        urls = imp.load_source('urls', os.path.join(settings['cwd'], "urls.py"))
    except IOError:
        log.msg("[!] There's no urls.py module valid in the project directory.")
        sys.exit(-1)

    sorted_urls = sorted(urls.urlpatterns,
                         key=lambda x: len(x[0].split("/")))

    for path, Resource in sorted_urls:
        node = root

        splitted = path.split("/")
        if splitted[-1] == "":
            splitted = splitted[:-1]

        for path in splitted[:-1]:
            if path not in node.next_resources:
                node.next_resources[path] = LupuloResource({})
            node = node.next_resources[path]

        last = splitted[-1]
        node.next_resources[last] = Resource({})

    for path, resource in root.next_resources.items():
        root.putChild(path, resource)


def get_website(sse_resource):
    """
        Return the Site for the web server.
    """
    root = Root({})
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

    testing = File(os.path.join(settings["lupulo_cwd"], 'tests/frontend'))
    root.putChild('lupulo_testing', testing)

    return server.Site(root)
