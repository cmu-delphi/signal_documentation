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

    name = Sequence(lambda n: f'datasource_name_{n}')
    display_name = Sequence(lambda n: f'datasource_display_name_{n}')


class SourceSubdivisionFactory(DjangoModelFactory):
    """
    A factory for the SourceSubdivision model.
    """
    class Meta:
        model = SourceSubdivision

    name = Sequence(lambda n: f'subdivision_name_{n}')
    display_name = Sequence(lambda n: f'subdivision_display_name_{n}')
    description = fake.text(max_nb_chars=250)
    db_source = fake.word()
    data_source = SubFactory(DataSourceFactory)
