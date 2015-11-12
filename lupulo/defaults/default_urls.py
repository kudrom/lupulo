# You should import all your Resources and put them here in a tuple of the form:
# urlpatterns = [
#     ('url/to/my/resource', MyResource),
# ]
from lupulo.resource import LupuloResource

class HelloResource(LupuloResource):
    def render_GET(self, request):
        return "Hello world"

class MundoResource(LupuloResource):
    def render_GET(self, request):
        return "Mundo sano"


urlpatterns = [
    ('hello', HelloResource),
    ('hola/buen/mundo', MundoResource)
]
