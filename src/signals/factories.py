from factory import (
    Sequence,
    SubFactory,
    post_generation,
)
from factory.django import DjangoModelFactory
from faker import Faker

from base.factories import LinkFactory
from datasources.factories import SourceSubdivisionFactory
from signals.models import (
    FormatChoices,
    Geography,
    HighValuesAreChoices,
    Pathogen,
    Signal,
    SignalCategory,
    SignalType,
    TimeLabelChoices,
    TimeTypeChoices,
)

fake = Faker()


class GeographyFactory(DjangoModelFactory):
    """
    A factory for the Geography model.
    """
    class Meta:
        model = Geography

    name = Sequence(lambda n: f'{n}')


class PathogenFactory(DjangoModelFactory):
    """
    A factory for the Pathogen model.
    """
    class Meta:
        model = Pathogen

    name = Sequence(lambda n: f'{n}')


class SignalCategoryFactory(DjangoModelFactory):
    """
    A factory for the SignalCategory model.
    """
    class Meta:
        model = SignalCategory

    name = Sequence(lambda n: f'{n}')


class SignalTypeFactory(DjangoModelFactory):
    """
    A factory for the SignalType model.
    """
    class Meta:
        model = SignalType

    name = Sequence(lambda n: f'{n}')


class SignalFactory(DjangoModelFactory):
    """
    A factory for the Signal model.
    """
    name = Sequence(lambda n: f'{n}')
    active = fake.boolean()
    short_description = fake.text(max_nb_chars=500)
    description = fake.text(max_nb_chars=500)
    format = fake.random_element(FormatChoices.values)
    time_type = fake.random_element(TimeTypeChoices.values)
    time_label = fake.random_element(TimeLabelChoices.values)
    category = SubFactory(SignalCategoryFactory)
    is_smoothed = fake.boolean()
    is_weighted = fake.boolean()
    is_cumulative = fake.boolean()
    has_stderr = fake.boolean()
    high_values_are = fake.random_element(HighValuesAreChoices.values)
    source = SubFactory(SourceSubdivisionFactory)

    class Meta:
        model = Signal

    @post_generation
    def generate_pathogens(self, create, extracted, **kwargs):
        if not create or not extracted:
            for _ in range(fake.random_int(min=1, max=10)):
                self.pathogen.add(PathogenFactory())
            return

    @post_generation
    def generate_signal_types(self, create, extracted, **kwargs):
        if not create or not extracted:
            for _ in range(fake.random_int(min=1, max=10)):
                self.signal_type.add(SignalTypeFactory())
            return

    @post_generation
    def generate_links(self, create, extracted, **kwargs):
        if not create or not extracted:
            for _ in range(fake.random_int(min=1, max=10)):
                self.links.add(LinkFactory())
            return

    @post_generation
    def generate_available_geography(self, create, extracted, **kwargs):
        if not create or not extracted:
            for _ in range(fake.random_int(min=1, max=10)):
                self.available_geography.add(GeographyFactory())
            return
