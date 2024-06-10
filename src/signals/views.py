from typing import Any, Dict

from django.conf import settings
from django.views.generic import DetailView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from signals.filters import SignalFilter
from signals.forms import SignalFilterForm
from signals.models import Signal, GeographicScope
from signals.serializers import SignalSerializer


class SignalsListView(ListView):
    """
    ListView for displaying a list of Signal objects.
    """

    model = Signal
    template_name = "signals/signals.html"
    paginate_by: int = settings.PAGE_SIZE

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
            "order_by": self.request.GET.get("order_by"),
            "pathogen": [int(el) for el in self.request.GET.getlist("pathogen")],
            "active": [el for el in self.request.GET.getlist("active")],
            "available_geography": [
                int(el) for el in self.request.GET.getlist("available_geography")
            ]
            if self.request.GET.get("available_geography")
            else None,
            "signal_type": [int(el) for el in self.request.GET.getlist("signal_type")]
            if self.request.GET.get("signal_type")
            else None,
            "geographic_scope": [el for el in self.request.GET.getlist("geographic_scope")]
            if self.request.GET.get("geographic_scope")
            else None,
            "source": [int(el) for el in self.request.GET.getlist("source")],
            "time_type": [el for el in self.request.GET.getlist("time_type")],
            "base_signal": self.request.GET.get("base_signal"),
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
        if not url_params_dict.get("geographic_scope"):
            url_params_dict["geographic_scope"] = [GeographicScope.objects.get(name="USA").id]
        context["url_params_dict"] = url_params_dict
        context["form"] = SignalFilterForm(initial=url_params_dict)
        context["url_params_str"] = url_params_str
        context["filter"] = SignalFilter(self.request.GET, queryset=self.get_queryset())

        context["signals"] = self.get_queryset()
        return context


class SignalsDetailView(DetailView):
    """
    DetailView for displaying a single Signal object.
    """

    model = Signal

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """
        Get the context data for the view.

        Returns:
            Dict[str, Any]: The context data for the view.
        """

        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["epivis_url"] = settings.EPIVIS_URL
        context["data_export_url"] = settings.DATA_EXPORT_URL
        return context


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
        "base",
        "source__name",
        "time_label",
        "geographic_scope__name",
    )
