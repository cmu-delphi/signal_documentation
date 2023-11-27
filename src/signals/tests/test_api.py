from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from signals.models import Signal
from signals.tests.factories import SignalFactory

fake = Faker()


class SignalListApiViewTest(APITestCase):

    def setUp(self):
        for i in range(fake.random_int(min=1, max=100)):
            SignalFactory()

    def test_signal_list_api_view(self):
        response = self.client.get(reverse('signals_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], Signal.objects.count())

    def test_signal_list_api_view_filters(self):
        signal = Signal.objects.order_by("?").first()
        signal.base = signal
        signal.save()
        response = self.client.get(reverse('signals_api'), {'name': signal.name})
        for result in response.json()['results']:
            self.assertEqual(signal.name, result['name'])
        response = self.client.get(reverse('signals_api'), {'pathogen__name': signal.pathogen.first().name})
        for result in response.json()['results']:
            self.assertTrue(signal.pathogen.first().name in result['pathogen'])
        response = self.client.get(reverse('signals_api'), {'available_geography__name': signal.available_geography.first().name})
        for result in response.json()['results']:
            self.assertTrue(signal.available_geography.first().name in result['available_geography'])
        response = self.client.get(reverse('signals_api'), {'signal_type__name': signal.signal_type.first().name})
        for result in response.json()['results']:
            self.assertTrue(signal.signal_type.first().name in result['signal_type'])
        response = self.client.get(reverse('signals_api'), {'category__name': signal.category.name})
        for result in response.json()['results']:
            self.assertTrue(signal.category.name in result['category'])
        response = self.client.get(reverse('signals_api'), {'source__name': signal.source.name})
        for result in response.json()['results']:
            self.assertTrue(signal.source.name in result['source'])
        response = self.client.get(reverse('signals_api'), {'time_label': signal.time_label})
        for result in response.json()['results']:
            self.assertEqual(signal.time_label, result['time_label'])
        response = self.client.get(reverse('signals_api'), {'format_type': signal.format_type})
        for result in response.json()['results']:
            self.assertEqual(signal.format_type, result['format_type'])
        response = self.client.get(reverse('signals_api'), {'base': signal.base.id})
        for result in response.json()['results']:
            self.assertEqual(signal.base.id, result['base']['id'])
