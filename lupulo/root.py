import os.path
from twisted.web import server
from twisted.web.static import File

from lupulo.resource import LupuloResource
from lupulo.exceptions import UrlInvalid

from settings import settings
import urls


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
    reload(urls)
    try:
        urlpatterns = urls.urlpatterns
    except AttributeError:
        raise UrlInvalid("There's no urlpatterns attribute in urls.py")

    sorted_urls = sorted(urls.urlpatterns,
                         key=lambda x: len(x[0].split("/")))

    if len(sorted_urls) > 0 and len(sorted_urls[0]) != 2:
        msg = "Each entry in urlpatterns should be a tuple of two elements"
        raise UrlInvalid(msg)

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
