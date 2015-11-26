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

This resource must inherit from *lupulo.http.LupuloResource* and can ask for
some template with the method *get_template*.

.. py:function:: get_template(path)

    Returns a LupuloTemplate for the path given as an argument

    :param string path: valid file path for a given template in the templates
                        folder

.. warning::

    The get_template function can only be called inside the render_* family
    methods.

Once the resource has the template it will call its *render* method and **return
what this method returns**.

.. py:function:: render(context={})

    Renders a template with the given context and returns a string.

    :param context dict: jinja2 context object used to render the template.

So for example, this are two valid lupulo resources binded in the urls.py to
some url

.. code-block:: python

    # urls.py file

    from lupulo.http import LupuloResource

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

Base.html
*********

One of this templates is **base.html**, which defines the following jinja2
blocks:

#. **title**: inside the title tag.
#. **css**: at the end of the head tag.
#. **body**: at the beginning of the body tag.
#. **anchors**: inside the body block, see below for more information.
#. **controller**: at the end of the body tag, just before the widgets tag.
#. **widgets**: at the end of the body tag.

You should define the **title** block to put your own title to the page and also
the **css** block if you want to define your own styles or include your own
stylesheets into the web page.

You shouldn't overwrite the **body** block unless you're very sure about it
because you are going to break some functionality of the framework unless you
provide it yourself. If you want to include your own content into the web page,
you should define the **anchors** block.

You can define your own controller of the events received from the backend by
overwriting the **controller** block, but usually you only want to include some
widgets and probably some js file of your own, you should do that defining the
**widgets** block.

debug_base.html
***************

Another base template is **debug_base.html**, which inherits at the same time 
from base.html. This template doesn't define any new block but provides all the
functionality to serve the debug web page rendered by the default template
debug.html.

You must extend the widgets block in this last template whenever you want to
debug a new widget which isn't provided by the framework.

Controller
----------

Each web page must have a controller that does the following:

#. Receives the data that the backend is sending through three sse events
   called *new_devices*, *new_widgets* and *new_event_sources*.
#. Provides a way to register widgets through the *register_widget* interface.
#. Provides a callback for onchange DOM event for the #device select form.
#. Provides a global object called lupulo_controller which is used thought the
   entire framework to access some of the above functionalities.

The default backend does this and provides a public API to allow easy
overwriting or modification of some or all of its responsibilities.

So if you want to modify the behaviour of the default controller, maybe to
expand its capabilities or to redefine it, you need to:

#. Overwrite the controller block of the base template you are using.
#. Create a controller and bind it to lupulo_controller.

You can overwrite completely the controller and provide all of the behaviour
yourself, but most of the time you only want to provide some code of your own
and then call the default implementation of the default controller.

Therefore, the usual use case is to overwrite the controller block as said
above, to construct a default controller, to connect some of the backend
callbacks to your own functions and then to call, in your custom callback, the
lupulo controller callback.

Or, said with code, imagine you have overwritten the controller block with this
piece of js code:

.. code-block:: javascript

    function new_widgets(event){
        // Some interesting custom logic

        lupulo_controller.new_widgets(event);
    }

    lupulo_controller = new DefaultController();
    lupulo_controller.setup();
    lupulo_controller.data_pipe.addEventListener("new_widgets", new_widgets);
    lupulo_controller.data_pipe.addEventListener("new_devices", lupulo_controller.new_devices);

.. note::

    The data_pipe object is a usual JS EventSource object used to communicate with
    the backend.

So, in this example you have built the controller and bound it to the
lupulo_controller name, you also have called its setup method (you always have
to do this), and finally you have overwritten both the *new_widgets* and the
*new_devices* sse events to you own callback and to the default implementation
respectively.

Finally, one piece of advice, to overwrite the controller is an advance
technique so if you don't understand how everything is working you should read
the source code of the controller default implementation in
*lupulo/static/js/controller.js* and a redefinition of it in
*lupulo/static/js/debug.js* for the debug page in *lupulo/templates/debug.html*,
hopefully you will understand everything once you have finished that lecture.
The paths are relative to the main project directory, the one you get when you
clone the project from github.

Error templates
---------------

Finally, if you want you can add your own custom templates for http related
errors in the templates directory. They must have the name of the status http
code associated with the error and they will be rendered whenever there is some
problem in the server related to that status code.

For example, if you want to add your own template when the user wants to access
a url that is not in the sitemap, you can add a *404.html* template in the
*templates/errors* directory of the project.

Only base templates of lupulo and templates in the errors directory will be used
to resolve inheritance when an error template is needed.

.. warning::

    Currently only 404 errors are rendered throguh this mechanism.
