from typing import Any, Dict

from django.conf import settings
from django.core.paginator import Page, Paginator
from django.views.generic import DetailView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from signals.filters import SignalFilter
from signals.forms import SignalFilterForm
from signals.models import Pathogen, Signal
from signals.serializers import SignalSerializer


class SignalsListView(ListView):
    """
    ListView for displaying a list of Signal objects.
    """

    model = Signal
    template_name = "signals/signals.html"
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
        url_params_dict = {
            "id": self.request.GET.get("id"),
            "search": self.request.GET.get("search"),
            "pathogen": [el for el in self.request.GET._getlist("pathogen")]
            if self.request.GET.get("pathogen")
            else [el.id for el in Pathogen.objects.all()],
            "active": [el for el in self.request.GET._getlist("active")]
            if self.request.GET.get("active")
            else [True, False],
            "available_geography": [
                int(el) for el in self.request.GET._getlist("available_geography")
            ]
            if self.request.GET.get("available_geography")
            else None,
            "signal_type": [int(el) for el in self.request.GET._getlist("signal_type")]
            if self.request.GET.get("signal_type")
            else None,
            "category": self.request.GET._getlist("category")
            if self.request.GET.get("category")
            else None,
            "format_type": [el for el in self.request.GET._getlist("format_type")],
            "source": [int(el) for el in self.request.GET._getlist("source")],
            "time_label": [el for el in self.request.GET._getlist("time_label")]
        }
        url_params_str = ""
        for param_name, param_value in url_params_dict.items():
            if isinstance(param_value, list):
                for value in param_value:
                    url_params_str = f"{url_params_str}&{param_name}={value}"
            else:
                if param_value not in ["", None]:
                    url_params_str = f"{url_params_str}&{param_name}={param_value}"
        return url_params_dict, url_params_str

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Get the context data for the view.

        Returns:
            Dict[str, Any]: The context data for the view.
        """

        context: Dict[str, Any] = super().get_context_data(**kwargs)
        url_params_dict, url_params_str = self.get_url_params()
        context["form"] = SignalFilterForm(initial=url_params_dict)
        context["url_params_str"] = url_params_str
        context["filter"] = SignalFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number: str | None = self.request.GET.get("page")
        page_obj: Page = paginator.get_page(page_number)

        context["signals"] = page_obj
        return context

    def get_template_names(self) -> list[str]:
        if self.request.htmx:
            return ["signals/signals_list.html"]
        return [self.template_name]


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
    search_fields = ("name", "display_name", "description", "short_description")
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = (
        "name",
        "display_name",
        "pathogen__name",
        "available_geography__name",
        "signal_type__name",
        "category__name",
        "format_type",
        "base",
        "source__name",
        "time_label",
    )
