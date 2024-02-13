from django.views.generic import ListView

from datasources.models import DataSource


class DataSourceListView(ListView):
    """
    ListView for displaying a list of DataSource objects.
    """

    model = DataSource
    template_name = "datasources/datasource_list.html"
