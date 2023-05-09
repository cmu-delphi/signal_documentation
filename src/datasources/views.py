from django.views.generic import ListView

from signals.models import Signal


class MainView(ListView):

    model = Signal
    template_name = 'datasources/signal_list.html.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signals'] = self.get_queryset()
        return context
