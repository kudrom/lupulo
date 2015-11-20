# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

import os.path

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
        return ErrorPage(404)


class LupuloTemplate(object):
    """
        Adapter around a jinja2 template which will render the template in an
        asynchronous way.
    """
    def __init__(self, template):
        self.template = template

    def render(self, context={}):
        utext = self.template.render(**context)
        text = utext.encode('ascii', 'ignore')
        return text


class ErrorPage(LupuloResource):
    """
        Base class for every error page in lupulo.
    """
    def __init__(self, code):
        LupuloResource.__init__(self, {})
        self.code = code
        directories = []
        directories.append(os.path.join(settings['templates_dir'], 'errors'))
        directories.append(os.path.join(settings['lupulo_templates_dir'], 'errors'))
        directories.append(settings['lupulo_templates_dir'])
        loader = FileSystemLoader(directories)
        options = {"auto_reload": True, "autoescape": True}
        self.environment = Environment(loader=loader, **options)

    def render(self, request):
        request.setResponseCode(self.code)
        request.setHeader("content-type", "text/html")
        template = self.get_template(str(self.code) + '.html')
        return template.render()
