from typing import Any, Dict

from django.conf import settings
from django.core.paginator import Page, Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from signals.filters import SignalFilter
from signals.models import Signal
from signals.serializers import SignalSerializer


class SignalsListView(ListView):
    """
    ListView for displaying a list of Signal objects.
    """

    model = Signal
    template_name = 'signals/signal_list.html'
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self) -> Any:
        """
        Get the queryset for the view.

        Returns:
            QuerySet: The queryset for the view.
        """

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
        """
        Get the context data for the view.

        Returns:
            Dict[str, Any]: The context data for the view.
        """

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
    """
    DetailView for displaying a single Signal object.
    """

    model = Signal


class SignalsListApiView(ListAPIView):
    """
    ListAPIView for retrieving a list of Signal objects via API.
    """

    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
    search_fields = ('name', 'display_name', 'description', 'short_description')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = (
        'name',
        'display_name',
        'pathogen__name',
        'available_geography__name',
        'signal_type__name',
        'category__name',
        'format_type',
        'base',
        'source__name',
        'time_label',
    )
