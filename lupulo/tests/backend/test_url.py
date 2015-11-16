import os.path
import shutil

from twisted.trial import unittest
from mock import MagicMock, call

from lupulo.settings import settings
from lupulo.exceptions import UrlInvalid, InvalidResource
from lupulo.root import connect_user_urls


URLS = '../urls.py'


class TestsUrls(unittest.TestCase):
    """
        To be runned properly, a urls.py file must be in the root directory of
        the project.
    """
    def setUp(self):
        settings['cwd'] = os.path.join(settings['lupulo_cwd'],
                                       'tests/backend/urls')
        settings['templates_dir'] = os.path.join(settings['cwd'], "templates")

        self.root_mock = MagicMock()
        self.root_mock.next_resources = {}
        self.root_mock.putChild = MagicMock()

    def tearDown(self):
        del settings['cwd']
        del settings['templates_dir']
        if os.path.exists(URLS):
            with open(URLS, "w+") as fp:
                fp.write("")
        if os.path.exists(URLS + 'c'):
            os.remove(URLS + 'c')

    def create_urls_file(self, filepath):
        src = os.path.join(settings['cwd'], filepath)
        with open(URLS, 'w+') as fp_urls:
            with open(src) as fp_mocked:
                text = "".join(fp_mocked.readlines())
                fp_urls.write(text)

    # This test needs to be executed first
    def test_aa_no_urlpatterns(self):
        self.create_urls_file('no_urlpatterns.py')
        self.assertRaises(UrlInvalid, connect_user_urls, self.root_mock)

    def test_simple_url_with_slash(self):
        self.create_urls_file('simple_url.py')
        connect_user_urls(self.root_mock)

        self.assertEqual(len(self.root_mock.next_resources), 1)
        self.assertEqual(set(self.root_mock.next_resources), set(['hello']))

        resource = self.root_mock.next_resources['hello']
        self.assertEqual(resource.render_GET(None), 'Hello world')

        self.root_mock.putChild.assert_called_once_with('hello', resource)

    def test_url_siblings(self):
        self.create_urls_file('siblings_urls.py')
        connect_user_urls(self.root_mock)

        self.assertEqual(len(self.root_mock.next_resources), 2)
        self.assertEqual(set(self.root_mock.next_resources),
                         set(['hello', 'bye']))
        self.assertEqual(self.root_mock.putChild.call_count, 2)
        bye = self.root_mock.next_resources['bye']
        self.assertEqual(len(bye.next_resources), 0)
        self.assertEqual(bye.render_GET(None), 'Bye world')

        hello = self.root_mock.next_resources['hello']
        self.assertEqual(len(hello.next_resources), 2)
        self.assertEqual(set(hello.next_resources), set(['world', 'death']))
        self.assertEqual(hello.render_GET(None), 'Hello world')

        self.assertEqual(len(hello.next_resources['world'].next_resources), 0)
        self.assertEqual(hello.next_resources['world'].render_GET(None),
                         'The world is amazing')

        self.assertEqual(len(hello.next_resources['death'].next_resources), 0)
        self.assertEqual(hello.next_resources['death'].render_GET(None),
                         'The death is scary')

        self.assertEqual(self.root_mock.putChild.call_args_list,
                         [call('bye', bye), call('hello', hello)])

    def test_gaps_url(self):
        self.create_urls_file('gaps_urls.py')
        connect_user_urls(self.root_mock)

        resource = self.root_mock
        self.assertEqual(resource.next_resources.keys(), ['hello'])

        resource = resource.next_resources['hello']
        self.assertEqual(resource.__class__.__name__, 'LupuloResource')
        self.assertEqual(resource.next_resources.keys(), ['world'])

        resource = resource.next_resources['world']
        self.assertEqual(resource.__class__.__name__, 'LupuloResource')
        self.assertEqual(resource.next_resources.keys(), ['this'])

        resource = resource.next_resources['this']
        self.assertEqual(resource.__class__.__name__, 'CustomResource')
        self.assertEqual(resource.next_resources.keys(), ['is'])

        resource = resource.next_resources['is']
        self.assertEqual(resource.__class__.__name__, 'LupuloResource')
        self.assertEqual(resource.next_resources.keys(), ['kudrom'])

        resource = resource.next_resources['kudrom']
        self.assertEqual(resource.__class__.__name__, 'CustomResource')
        self.assertEqual(len(resource.next_resources), 0)

    def test_repeated_url(self):
        self.create_urls_file('repeated_url.py')
        connect_user_urls(self.root_mock)

        self.assertEqual(self.root_mock.next_resources.keys(), ['death'])
        resource = self.root_mock.next_resources['death']
        self.assertEqual(resource.render_GET(None), 'The death is scary')

    def test_invalid_tuple(self):
        self.create_urls_file('dictionary_url.py')
        self.assertRaises(UrlInvalid, connect_user_urls, self.root_mock)

    def test_invalid_resource(self):
        self.create_urls_file('invalid_resource.py')
        self.assertRaises(InvalidResource, connect_user_urls, self.root_mock)
