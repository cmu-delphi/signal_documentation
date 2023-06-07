from django.urls import path

from signals.views import SignalsDetailView, SignalsListView

urlpatterns = [
    path('', SignalsListView.as_view(), name='signals'),
    path('signals/<pk>/', SignalsDetailView.as_view(), name='signal'),
]
