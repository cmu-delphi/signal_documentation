from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker

from base.models import Link, LinkTypeChoices

fake = Faker()


class LinkFactory(DjangoModelFactory):
    """
    A factory for the Link model.
    """
    class Meta:
        model = Link

    link_type = fake.random_element(LinkTypeChoices.values)
    url = Sequence(lambda n: f'http://www.{n}.org/')
