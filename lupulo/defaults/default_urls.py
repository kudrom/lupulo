# You should import all your Resources and put them here in a tuple of the form:
# urlpatterns = [
#     ('url/to/my/resource', MyResource),
# ]
from lupulo.root import LupuloResource

class HolaResource(LupuloResource):
    def render_GET(self, request):
        return "Hola mundo"

class MundoResource(LupuloResource):
    def render_GET(self, request):
        return "Mundo sano"


urlpatterns = [
    ('hola', HolaResource),
    ('hola/buen/mundo', MundoResource)
]
