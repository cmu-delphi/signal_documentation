from django.test import TestCase

from datasources.tests.factories import DataSourceFactory, SourceSubdivisionFactory


class SourceSubdivisionModelTest(TestCase):

    def setUp(self) -> None:
        self.source_subdivision = SourceSubdivisionFactory()

    def test_source_subdivision_str(self) -> None:
        self.assertEqual(self.source_subdivision.__str__(), self.source_subdivision.name)


class DataSourceModelTest(TestCase):

    def setUp(self) -> None:
        self.data_source = DataSourceFactory()

    def test_data_source_str(self) -> None:
        self.assertEqual(str(self.data_source), self.data_source.name)
