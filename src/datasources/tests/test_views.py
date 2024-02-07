from django.test import TestCase
from django.urls import reverse
from faker import Faker

from datasources.models import DataSource
from datasources.tests.factories import DataSourceFactory

fake = Faker()


class DataSourceListViewTest(TestCase):

    def setUp(self):
        for _ in range(fake.random_int(min=1, max=100)):
            DataSourceFactory()

    def test_datasource_list_view(self):
        response = self.client.get(reverse('datasources'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'datasources/datasource_list.html')
        self.assertTrue('datasource_list' in response.context)
        self.assertEqual(response.context['datasource_list'].count(), DataSource.objects.count())
