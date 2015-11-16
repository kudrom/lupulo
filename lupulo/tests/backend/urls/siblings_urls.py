from lupulo.http import LupuloResource


class HelloResource(LupuloResource):
    def render_GET(self, request):
        return "Hello world"


class ByeResource(LupuloResource):
    def render_GET(self, request):
        return "Bye world"


class WorldResource(LupuloResource):
    def render_GET(self, request):
        return "The world is amazing"


class DeathResource(LupuloResource):
    def render_GET(self, request):
        return "The death is scary"


urlpatterns = [
    ("hello/world", WorldResource),
    ("hello/death", DeathResource),
    ("hello", HelloResource),
    ("bye", ByeResource),
]
