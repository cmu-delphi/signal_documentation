from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from faker import Faker

from base.models import Link
from signals.models import Signal
from signals.tests.factories import SignalFactory

fake = Faker()


class SignalListViewTest(TestCase):

    def setUp(self):
        for _ in range(fake.random_int(min=1, max=100)):
            SignalFactory()

    def test_signals_view(self):
        response = self.client.get(reverse('signals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signals/signals.html')

    def test_signals_view_context(self):
        response = self.client.get(reverse('signals'))
        self.assertTrue('signals' in response.context)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('filter' in response.context)

    def test_signals_view_filters(self):
        signal = SignalFactory()
        response = self.client.get(reverse('signals'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), Signal.objects.count())
        response = self.client.get(reverse('signals'), {'pathogen': signal.pathogen.first().id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), 1)
        self.assertEqual(response.context['filter'].qs.first(), signal)
        response = self.client.get(reverse('signals'), {'available_geography': signal.available_geography.first().id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), 1)
        self.assertEqual(response.context['filter'].qs.first(), signal)
        response = self.client.get(reverse('signals'), {'signal_type': signal.signal_type.first().id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), 1)
        self.assertEqual(response.context['filter'].qs.first(), signal)
        response = self.client.get(reverse('signals'), {'category': signal.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), 1)
        self.assertEqual(response.context['filter'].qs.first(), signal)
        response = self.client.get(reverse('signals'), {'source': signal.source.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), 1)
        self.assertEqual(response.context['filter'].qs.first(), signal)
        response = self.client.get(reverse('signals'), {'time_label': signal.time_label})
        self.assertEqual(response.status_code, 200)
        for s in response.context['filter'].qs:
            self.assertEqual(s.time_label, signal.time_label)

    def test_signals_view_search(self):
        name = fake.random_element(Signal.objects.all()).name
        description_word = fake.random_element(fake.random_element(Signal.objects.all()).description.split(' ')).strip()
        short_description_word = fake.random_element(fake.random_element(Signal.objects.all()).short_description.split(' ')).strip()
        response = self.client.get(reverse('signals'),  {'search': ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), Signal.objects.count())
        response = self.client.get(reverse('signals'), {'search': name})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter'].qs.count(), 1)
        self.assertEqual(response.context['filter'].qs.first().name, name)
        response = self.client.get(reverse('signals'), {'search': description_word})
        self.assertEqual(response.status_code, 200)
        for s in response.context['filter'].qs:
            self.assertTrue(description_word in s.description)
        response = self.client.get(reverse('signals'), {'search': short_description_word})
        self.assertEqual(response.status_code, 200)
        for s in response.context['filter'].qs:
            self.assertTrue(short_description_word in s.short_description)


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}})
class SignalDetailViewTest(TestCase):

    def setUp(self):
        self.signal = SignalFactory()

    def test_signal_detail_view(self):
        with patch.object(Link, 'get_preview'):
            response = self.client.get(reverse('signal', kwargs={'pk': self.signal.id}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'signals/signal_detail.html')

    def test_signal_detail_view_context(self):
        with patch.object(Link, 'get_preview'):
            response = self.client.get(reverse('signal', kwargs={'pk': self.signal.id}))
            self.assertTrue('signal' in response.context)
            self.assertEqual(response.context['signal'], self.signal)
