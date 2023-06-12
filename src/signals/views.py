from django.core.paginator import Paginator
from django.views.generic import ListView

from signals.filters import SignalFilter
from signals.models import Signal


class SignalsListView(ListView):

    model = Signal
    template_name = 'signals/signal_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        f = SignalFilter(self.request.GET, queryset=queryset)
        return f.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = SignalFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['signals'] = page_obj
        return context
