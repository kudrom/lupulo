.. _templates:

Templates
=========

You can also write your own web pages and serve them in a custom sitemap using
the templates abstraction.

A template is a jinja2 text file in the templates directory of the project,
which will be compiled by the backend to html and served to the user in a
specific url that you define in the urls.py file of your project.

The urls.py file must contain a list named urlpatterns made of tuples of two
elements. The first element is a string that defines the url that a `twisted
resource
<https://twistedmatrix.com/documents/15.0.0/web/howto/using-twistedweb.html#resource-objects>`_
(which is the second element) will listen to and render some information.

This resource must inherit from *lupulo.resource.LupuloResource* and can ask for
some template with the method *get_template*.

.. py:function:: get_template(path)

    Returns a LupuloTemplate for the path given as an argument

    :param string path: valid file path for a given template in the templates
                        folder

Once the resource has the template it will call its *render* method without any
arguments and **return what this method returns**.

So for example, this are two valid lupulo resources binded in the urls.py to
some url

.. code-block:: python

    # urls.py file

    from lupulo.resource import LupuloResource

    class HelloResource(LupuloResource):
        def render_GET(self, request):
            return "Hello world"

    class TemplateResource(LupuloResource):
        def render_GET(self, request):
            template = self.get_template('hello.html')
            return template.render()


    urlpatterns = [
        ('hello', HelloResource),
        ('hello/template', TemplateResource)
    ]

Inheritance
-----------

Any template can inherit from a set of lupulo templates that are designed to
ease the development of your project.

One of this templates is base.html, which defines the following jinja2 blocks:

#. **title**: inside the title tag.
#. **css**: at the end of the head tag.
#. **body**: at the beginning of the body tag.
#. **scripts**: at the end of the body tag.