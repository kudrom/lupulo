from setuptools import setup, find_packages

version = "0.1"
description = """
    **lupulo** is a final project of a university degree in software engineering
    that is supposed to be a framework that will allow embedded system
    programmers to build quick realtime web pages to monitor the state of its
    device.

    To see the entire documentation you should go to `ReadTheDocs
    <http://lupulo.readthedocs.org>`_.

    Enjoy!
    """

with open('README.rst') as f:
    readme = f.read()

with open('changelog.rst') as f:
    changelog = f.read()

setup(
    name = "lupulo",
    version = version,

    packages = find_packages(),
    package_dir = {'lupulo': 'lupulo'},
    package_data = {'lupulo': ['defaults/*.json', 'startup.tac',
                               'defaults/default_settings.py',
                               'defaults/static/js/*.js',
                               'defaults/static/js/widgets/*.js',
                               'defaults/static/css/*.css',
                               'defaults/templates/*.html']},
    scripts = ['bin/lupulo_start', 'bin/lupulo_create'],

    install_requires = ['pyserial', 'twisted', 'pymongo'],

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
