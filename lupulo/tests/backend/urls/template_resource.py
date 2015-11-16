from lupulo.http import LupuloResource


class TestingResource(LupuloResource):
    def render_GET(self, request):
        template = self.get_template('base.html')
        return template.render()

urlpatterns = [
    ('hello', TestingResource)
]
