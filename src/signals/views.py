from django.views.generic import ListView

from signals.filters import SignalFilter
from signals.models import Signal


class SignalsListView(ListView):

    model = Signal
    template_name = 'signals/signal_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        f = SignalFilter(self.request.GET, queryset=queryset)
        return f.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['signals'] = self.get_queryset()
        context['filter'] = SignalFilter(self.request.GET, queryset=self.get_queryset())
        return context
