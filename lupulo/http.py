# -*- encoding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

import os.path
from StringIO import StringIO

from twisted.web import resource, server
from twisted.internet import defer, reactor
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
        self.request = None

    def get_template(self, path):
        """
            Factory method to construct LupuloTemplates.
        """
        template = self.environment.get_template(path)
        return LupuloTemplate(template, self.request)

    def render(self, request):
        """
            Populates the Resource with the request of a web page to be able to
            render later the web page when the child calls get_template.
        """
        self.request = request
        return resource.Resource.render(self, request)

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
        The code to render asynchronously is from txtemplate.
    """
    def __init__(self, template, request):
        self.template = template
        self.request = request
        self._stream = None
        self.delayed_call = None
        self._buffer = StringIO()
        self.request = request

    def blocking_render(self, context={}):
        """
            Private API, only used when it's sure that the web page is
            very short.
        """
        utext = self.template.render(**context)
        text = utext.encode('ascii', 'ignore')
        return text

    def render(self, context={}):
        """
            Renders a web page in an asynchronous way.
        """
        iterator = self.template.generate(**context)
        self._deferred = defer.Deferred()
        self._deferred.addCallbacks(self._rendered_cb, self._failed_cb)
        delay = settings['template_async_call_delay']
        self.delayed_call = reactor.callLater(delay,
                                              self._populate_buffer, iterator)
        return server.NOT_DONE_YET

    def _close_delayed_callback(self):
        """
            Closes the delayed callback that is responsible for populating the
            buffer.
        """
        if self.delayed_call and self.delayed_call.active():
            self.delayed_call.cancel()

    def _populate_buffer(self, stream):
        """
            Renders the web page in small steps until it's done.
        """
        try:
            for x in xrange(settings['template_n_steps']):
                output = stream.next()
                self._buffer.write(output)
        except StopIteration, e:
            self._deferred.callback(None)
        except Exception, e:
            self._deferred.errback(e)
        else:
            delay = settings['template_async_call_delay']
            self.delayed_call = reactor.callLater(delay,
                                                  self._populate_buffer,
                                                  stream)

    def _failed_cb(self, reason):
        """
            For some reason the buffer failed when it was being populated.
        """
        log.msg(reason.getErrorMessage())
        self._close_delayed_callback()
        # TODO: this should be a 500 error
        return "Failed to render template"

    def _rendered_cb(self, _):
        """
            The page is entirely rendered, so write to the request its
            contents.
        """
        result = self._buffer.getvalue()
        self._buffer.close()
        self._buffer = None
        self._close_delayed_callback()

        content = result.encode('ascii', 'ignore')
        self.request.write(content)
        self.request.finish()


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
        return template.blocking_render()
