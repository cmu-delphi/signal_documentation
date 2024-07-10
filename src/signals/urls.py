from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.decorators.cache import cache_page

from signals.views import (
    SignalsDetailView,
    SignalsListApiView,
    SignalsListView,
)
from signal_documentation.settings import CACHE_TIME

urlpatterns: list[URLPattern] = [
    path('', cache_page(CACHE_TIME)(SignalsListView.as_view()), name='signals'),
    path('signals/<int:pk>/', SignalsDetailView.as_view(), name='signal'),
    path('signals/<pk>/', SignalsDetailView.as_view(), name='signal'),

    # REST API
    path('api/v1/signals/', SignalsListApiView.as_view(), name='signals_api'),
]
