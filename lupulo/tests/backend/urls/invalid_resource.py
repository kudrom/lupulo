class HelloResource(object):
    def render_GET(self, request):
        return "Hello world"


urlpatterns = [
    ("hello/", HelloResource)
]
