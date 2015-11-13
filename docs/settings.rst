.. _settings:

Settings
========

The settings is the main way the backend is configured. It's a valid python
module with a dictionary called settings inside of it that the entire framework
consults in order to take action.

.. warning::

    The settings dictionary must inherit from the lupulo.settings dictionary, so
    pay attention that at the beggining of the python module you can see
    settings = lupulo_settings

In the source file of the settings you can find some explanation for every
setting.
