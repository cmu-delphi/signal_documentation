from typing import Any, Dict

from django.core.paginator import Page, Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

from signals.filters import SignalFilter
from signals.models import Signal


class SignalsListView(ListView):

    model = Signal
    template_name = 'signals/signal_list.html'
    paginate_by = 10

    def get_queryset(self) -> Any:
        queryset = super().get_queryset()
        f = SignalFilter(self.request.GET, queryset=queryset)
        return f.qs

    def get_url_params(self):
        url_params_dict = dict()
        url_params_str = ""
        for param_name in self.request.GET:
            if param_name == "page":
                continue
            param_value = self.request.GET._getlist(param_name)
            if param_name != "search":
                url_params_dict[param_name] = [int(el) for el in param_value if el != ""]
                for v in param_value:
                    url_params_str = f"{url_params_str}&{param_name}={v}"
            else:
                url_params_dict[param_name] = self.request.GET[param_name]

        return url_params_dict, url_params_str

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['filter'] = SignalFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number: str | None = self.request.GET.get('page')
        page_obj: Page = paginator.get_page(page_number)
        context["url_params_dict"], context["url_params_str"] = self.get_url_params()
        context['signals'] = page_obj
        return context


@method_decorator(cache_page(60 * 5), name='dispatch')
class SignalsDetailView(DetailView):

    model = Signal
