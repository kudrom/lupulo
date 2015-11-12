from lupulo.root import LupuloResource


class HelloResource(LupuloResource):
    def render_GET(self, request):
        return "Hello world"


urlpatterns = [
    ("hello/", HelloResource)
]
