from setuptools import setup, find_packages

setup(
    name = "lupulo",
    version = "0.1",

    packages = find_packages(),
    package_dir = {'lupulo': 'lupulo'},
    package_data = {'lupulo': ['defaults/*.json', 'defaults/startup.tac',
                               'defaults/static/js/*.js',
                               'defaults/static/js/widgets/*.js',
                               'defaults/static/css/*.css',
                               'defaults/templates/*.html']},

    install_requires = ['pyserial', 'twisted', 'pymongo'],

    author = "kudrom",
    author_email = "kudrom@riseup.net",
    description = "Framework to build realtime web pages.",
    license = "GPL",
    keywords = "lupulo IoT realtime",
    url = "http://github.com/kudrom/lupulo",
)
