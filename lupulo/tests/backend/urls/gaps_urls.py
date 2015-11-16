from lupulo.http import LupuloResource


class CustomResource(LupuloResource):
    def render_GET(self, request):
        return "Something smart"


urlpatterns = [
    ("hello/world/this/is/kudrom", CustomResource),
    ("hello/world/this", CustomResource)
]
