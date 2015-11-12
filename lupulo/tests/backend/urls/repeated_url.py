from lupulo.resource import LupuloResource

class DeathResource(LupuloResource):
    def render_GET(self, request):
        return "The death is scary"


urlpatterns = [
    ('death', LupuloResource),
    ('death', DeathResource)
]
