from django.test import TestCase
from django.urls import reverse
from faker import Faker

from signals.factories import SignalFactory

fake = Faker()


class SignalListViewTest(TestCase):

    def setUp(self):
        for i in range(fake.random_int(min=1, max=100)):
            SignalFactory()

    def test_signal_list_view(self):
        response = self.client.get(reverse('signals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signals/signal_list.html')

    def test_signal_list_view_context(self):
        response = self.client.get(reverse('signals'))
        self.assertTrue('signals' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('filter' in response.context)

    def test_signal_list_view_filter_by_pathogen(self):
        signal = SignalFactory()
        response = self.client.get(reverse('signals'), {'pathogen': signal.pathogen.first().id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['signals'].count(), 1)
