from django.urls import path

from datasources.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]
