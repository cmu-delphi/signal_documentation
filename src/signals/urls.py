from django.urls import path

from signals.views import SignalsListView

urlpatterns = [
    path('', SignalsListView.as_view(), name='signals'),
]
