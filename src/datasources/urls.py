from django.urls import path
from django.urls.resolvers import URLPattern

from datasources.views import DataSourceListView

urlpatterns: list[URLPattern] = [
    path('', DataSourceListView.as_view(), name='datasources'),
]
