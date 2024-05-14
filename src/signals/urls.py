from django.urls import path
from django.urls.resolvers import URLPattern

from signals.views import (
    SignalsDetailView,
    SignalsListApiView,
    SignalsListView,
    GeographyUnitListApiView
)

urlpatterns: list[URLPattern] = [
    path('', SignalsListView.as_view(), name='signals'),
    path('signals/<int:pk>/', SignalsDetailView.as_view(), name='signal'),
    path('signals/<pk>/', SignalsDetailView.as_view(), name='signal'),

    # REST API
    path('api/v1/signals/', SignalsListApiView.as_view(), name='signals_api'),
    path('api/v1/geography_units/', GeographyUnitListApiView.as_view(), name='geography_units_api')
]
