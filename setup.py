# -*- coding: utf-8 -*-
# Copyright (C) 2015  Alejandro López Espinosa (kudrom)

from setuptools import setup, find_packages

version = "0.3"
description = """
    **lupulo** is a final project of a university degree in software engineering
    that is supposed to be a framework that will allow embedded system
    programmers to build quick realtime web pages to monitor the state of its
    device.

    To see the entire documentation you should go to `ReadTheDocs
    <http://lupulo.readthedocs.org>`_.

    Enjoy!
    """

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name = "lupulo",
    version = version,

    packages = find_packages(),
    package_dir = {'lupulo': 'lupulo'},
    package_data = {'lupulo': ['defaults/*.json', 'startup.tac',
                               'defaults/*.py',
                               'defaults/templates/*.html',
                               'defaults/static/css/*.css',
                               'static/js/*.js',
                               'static/js/widgets/*.js',
                               'static/css/*.css',
                               'templates/*.html',
                               'templates/errors/*.html',
                               'tests/frontend/*.html']},
    scripts = ['bin/lupulo_start', 'bin/lupulo_create', 'bin/lupulo_sse_client'],

    install_requires = requirements,

    author = "kudrom",
    author_email = "kudrom@riseup.net",
    description = "Framework to build realtime web pages dedicated to monitor \
                   robots or IoT devices.",
    long_description = description,
    license = "GPL",
    keywords = "lupulo IoT realtime",
    url = "http://github.com/kudrom/lupulo",
    classifiers = (
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Twisted",
        "Framework :: Sphinx",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 2",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Embedded Systems",
    )
)
