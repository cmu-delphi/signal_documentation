from django.urls import path

from base.views import ContactsView

urlpatterns = [
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
