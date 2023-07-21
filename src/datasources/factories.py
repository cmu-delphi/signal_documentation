from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from datasources.models import DataSource, SourceSubdivision

fake = Faker()


class DataSourceFactory(DjangoModelFactory):
    """
    A factory for the DataSource model.
    """
    class Meta:
        model = DataSource

    name = Sequence(lambda n: f'{n}')
    display_name = Sequence(lambda n: f'{n}')


class SourceSubdivisionFactory(DjangoModelFactory):
    """
    A factory for the SourceSubdivision model.
    """
    class Meta:
        model = SourceSubdivision

    name = Sequence(lambda n: f'{n}')
    display_name = Sequence(lambda n: f'{n}')
    description = fake.text()
    db_source = fake.word()
    data_source = SubFactory(DataSourceFactory)
