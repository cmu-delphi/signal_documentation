from django.db import models
from django.utils.translation import gettext_lazy as _
from models_extensions.models import TimeStampedModel


class SourceSubdivision(TimeStampedModel):
    """
    A model representing a source subdivision.
    """
    name: models.CharField = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )
    display_name: models.CharField = models.CharField(
        help_text=_('Display Name'),
        max_length=128,
        unique=True
    )
    external_name: models.CharField = models.CharField(
        help_text=_('External Name'),
        max_length=128,
        null=True,
    )
    description: models.TextField = models.TextField(
        help_text=_('Source description'),
        max_length=1000,
        null=True,
        blank=True
    )
    db_source: models.CharField = models.CharField(
        help_text=_('DB Source'),
        max_length=128,
    )
    links: models.ManyToManyField = models.ManyToManyField(
        'base.Link',
        help_text=_('Source Subdivision links'),
        related_name="source_subdivisions"
    )
    data_source: models.ForeignKey = models.ForeignKey(
        'datasources.DataSource',
        related_name='source_subdivisions',
        help_text=_('Source Subdivision'),
        on_delete=models.PROTECT
    )

    class Meta:
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the source subdivision as a string.

        :return: The name of the source subdivision as a string.
        :rtype: str
        """
        return str(self.name)


class DataSource(TimeStampedModel):
    """
    A model representing a data source.
    """

    name: models.CharField = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )
    display_name: models.CharField = models.CharField(
        help_text=_('Display Name'),
        max_length=128,
        unique=True
    )
    description: models.TextField = models.TextField(
        help_text=_('Source description'),
        max_length=1000,
        null=True,
        blank=True
    )

    source_license: models.ForeignKey = models.ForeignKey(
        'base.License',
        related_name='data_sources',
        help_text=_('License'),
        on_delete=models.PROTECT,
        null=True
    )

    links: models.ManyToManyField = models.ManyToManyField(
        'base.Link',
        help_text=_('DataSource links'),
        related_name="data_sources"
    )

    class Meta:
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the data source as a string.

        :return: The name of the data source as a string.
        :rtype: str
        """
        return str(self.name)
