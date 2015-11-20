# You should import all your Resources and put them here in a tuple of the form:
# urlpatterns = [
#     ('url/to/my/resource', MyResource),
# ]
from lupulo.http import LupuloResource
from lupulo.tests.backend.benchmarking import BenchmarkingResource

class HelloResource(LupuloResource):
    def render_GET(self, request):
        return "Hello world"


urlpatterns = [
    ('hello', HelloResource),
    ('benchmarking', BenchmarkingResource)
]
