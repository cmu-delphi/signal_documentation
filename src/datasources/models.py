from django.db import models
from django.utils.translation import gettext_lazy as _


class ReferenceSignalType(models.Model):
    """
    A model representing a reference signal.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the reference signal as a string.

        :return: The name of the reference signal as a string.
        :rtype: str
        """
        return self.name


class SourceSubdivision(models.Model):
    """
    A model representing a source subdivision.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )
    display_name = models.CharField(
        help_text=_('Display Name'),
        max_length=128,
        unique=True
    )
    description = models.TextField(
        help_text=_('Source description'),
        max_length=1000,
        blank=True
    )
    reference_signal = models.ForeignKey(
        'datasources.ReferenceSignalType',
        help_text=_('Reference Signal'),
        related_name='source_subdivisions',
        on_delete=models.PROTECT,
        null=True
    )
    db_source = models.CharField(
        help_text=_('DB Source'),
        max_length=128,
    )
    links = models.ManyToManyField(
        'base.Link',
        help_text=_('Source Subdivision links'),
        related_name="source_subdivisions"
    )
    data_source = models.ForeignKey(
        'datasources.DataSource',
        related_name='source_subdivisions',
        help_text=_('Source Subdivision'),
        on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        """
        Returns the name of the source subdivision as a string.

        :return: The name of the source subdivision as a string.
        :rtype: str
        """
        return self.name


class DataSource(models.Model):
    """
    A model representing a data source.
    """

    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )
    display_name = models.CharField(
        help_text=_('Display Name'),
        max_length=128,
        unique=True
    )
    description = models.TextField(
        help_text=_('Source description'),
        max_length=1000,
        blank=True
    )
    source_license = models.CharField(
        help_text=_('License'),
        max_length=128
    )
    links = models.ManyToManyField(
        'base.Link',
        help_text=_('DataSource links'),
        related_name="data_sources"
    )

    def __str__(self) -> str:
        """
        Returns the name of the data source as a string.

        :return: The name of the data source as a string.
        :rtype: str
        """
        return self.name
