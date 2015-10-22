from importlib import import_module

from m3dpi_ui.settings import settings
from m3dpi_ui.exceptions import NotListenerFound


def connect_listener(parent, sse_resource):
    """
        Load, instantiate and registers a Listener.
    """
    module_name = settings["listener"] + "_listener"
    try:
        module = import_module("m3dpi_ui.listeners.%s" % module_name)
    except ImportError as e:
        raise NotListenerFound(e.message.split(" ")[-1])

    # Find the Listener
    Listener = getattr(module, settings["listener"].capitalize() + "Listener")

    # Instantiate it and register towards the application
    listener = Listener(sse_resource)
    listener.setServiceParent(parent)
