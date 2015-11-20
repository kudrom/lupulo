import datetime

from lupulo.http import LupuloResource

from twisted.web import server


def timestamp():
    return float(datetime.datetime.now().strftime("%s"))


class BenchmarkingResource(LupuloResource):
    def render_GET(self, request):
        template = self.get_template('benchmarking.html')
        self.environment.globals['timestamp'] = timestamp

        context = {}
        context['big_list'] = []
        for i in range(4000000):
            context['big_list'].append(i)

        context['old_time'] = timestamp()
        self.request = request

        return template.render(request, context)
