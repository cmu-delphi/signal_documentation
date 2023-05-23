from django.views.generic import TemplateView

from base.models import ContactsConfiguration


class ContactsView(TemplateView):
    template_name = 'base/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts_info'] = ContactsConfiguration.get_solo()
        return context
