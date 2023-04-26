from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeTypeChoices(models.TextChoices):
    """
    A class representing choices for time types.
    """
    DAY = 'day', _('Day')
    WEEK = 'week', _('Week')


class TimeLabelChoices(models.TextChoices):
    """
    A class representing choices for time labels.
    """
    DAY = 'day', _('Day')
    DATE = 'date', _('Date')


class FormatChoices(models.TextChoices):
    """
    A class representing choices for formats.
    """
    RAW = 'raw', _('Raw')
    PERCENT = 'percent', _('Percent')
    FRACTION = 'fraction', _('Fraction')
    COUNT = 'count', _('Count')
    PER100K = 'per100k', _('Per 100K')


class CategoryChoices(models.TextChoices):
    """
    A class representing choices for categories.
    """
    PUBLIC = 'public', _('Public')
    EARLY = 'early', _('Early')
    CASES_TESTING = 'cases_testing', _('Case testing')
    LATE = 'late', _('Late')
    OTHER = 'other', _('Other')


class HighValuesAreChoices(models.TextChoices):
    """
    A class representing choices for high values.
    """
    BAD = 'bad', _('Bad')
    GOOD = 'good', _('Good')
    NEUTRAL = 'neutral', _('Neutral')


class SignalType(models.Model):
    """
    A model representing a signal type.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the signal type as a string.

        :return: The name of the signal type as a string.
        :rtype: str
        """
        return self.name


class Pathogen(models.Model):
    """
    A model representing a pathogen.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the pathogen as a string.

        :return: The name of the pathogen as a string.
        :rtype: str
        """
        return self.name


class Geography(models.Model):
    """
    A model representing a available geography.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the available geography as a string.

        :return: The name of the available geography as a string.
        :rtype: str
        """
        return self.name


class Signal(models.Model):
    """
    A model representing a signal.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )
    base_name = models.CharField(
        help_text=_('Signal BaseName'),
        max_length=128,
        unique=True
    )
    active = models.BooleanField(
        help_text=_('Active'),
        default=False
    )
    short_description = models.TextField(
        help_text=_('Short Description'),
        max_length=500,
        null=True,
        blank=True
    )
    description = models.TextField(
        help_text=_('Description'),
        max_length=1000,
        null=True,
        blank=True
    )
    time_type = models.CharField(
        help_text=_('Time type'),
        max_length=128,
        choices=TimeLabelChoices.choices
    )
    time_label = models.CharField(
        help_text=_('Time label'),
        max_length=128,
        choices=TimeLabelChoices.choices
    )
    format = models.CharField(
        help_text=_('Format'),
        max_length=128,
        choices=FormatChoices.choices
    )
    category = models.CharField(
        help_text=_('Category'),
        max_length=128,
        choices=CategoryChoices.choices
    )
    high_values_are = models.CharField(
        help_text=_('High values are'),
        max_length=128,
        choices=HighValuesAreChoices.choices
    )
    links = ArrayField(
        help_text=_('Links'),
        base_field=models.URLField(max_length=256),
        blank=True
    )
    available_geography = models.ManyToManyField(
        'Geography',
        help_text=_('Available geography')
    )
    pathogen = models.ForeignKey(
        'Pathogen',
        related_name='pathogen',
        help_text=_('Pathogen/Disease Area'),
        on_delete=models.SET_NULL,
        null=True
    )
    is_smoothed = models.BooleanField(
        help_text=_('Is Smoothed'),
        default=False
    )
    is_weighted = models.BooleanField(
        help_text=_('Is Weighted'),
        default=False
    )
    is_cumulative = models.BooleanField(
        help_text=_('Is Cumulative'),
        default=False
    )
    has_stderr = models.BooleanField(
        help_text=_('Has StdErr'),
        default=False
    )
    has_sample_size = models.BooleanField(
        help_text=_('Has Sample Size'),
        default=False
    )

    def __str__(self) -> str:
        """
        Returns the name of the signal as a string.

        :return: The name of the signal as a string.
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
    db_source = models.CharField(
        help_text=_('DB Source'),
        max_length=128,
        unique=True
    )
    source_subdivision = models.ForeignKey(
        'SourceSubdivision',
        help_text=_('Source Subdivision'),
        on_delete=models.PROTECT
    )
    description = models.TextField(
        help_text=_('Source description'),
        max_length=1000,
        null=True,
        blank=True
    )
    reference_signal = models.ForeignKey(
        'Signal',
        related_name='data_sources',
        help_text=_('Reference Signal'),
        on_delete=models.PROTECT
    )
    signal_type = models.ForeignKey(
        'SignalType',
        related_name='data_sources',
        help_text=_('Signal Type'),
        on_delete=models.SET_NULL,
        null=True
    )
    source_license = models.CharField(
        help_text=_('License'),
        max_length=128
    )
    dua = models.URLField(
        help_text=_('DUA'),
        max_length=256,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the data source as a string.

        :return: The name of the data source as a string.
        :rtype: str
        """
        return self.name
