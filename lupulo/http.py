from twisted.web import resource

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
