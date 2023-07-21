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
    WEEK = 'week', _('Week')


class FormatChoices(models.TextChoices):
    """
    A class representing choices for formats.
    """
    RAW = 'raw', _('Raw')
    PERCENT = 'percent', _('Percent')
    FRACTION = 'fraction', _('Fraction')
    COUNT = 'count', _('Count')
    PER100K = 'per100k', _('Per 100K')


class HighValuesAreChoices(models.TextChoices):
    """
    A class representing choices for high values.
    """
    BAD = 'bad', _('Bad')
    GOOD = 'good', _('Good')
    NEUTRAL = 'neutral', _('Neutral')


class SignalCategory(models.Model):
    """
    A model representing a signal category.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the signal category as a string.

        :return: The name of the signal category as a string.
        :rtype: str
        """
        return self.name


class SignalType(models.Model):
    """
    A model representing a signal type.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    class Meta:
        ordering = ["name"]

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

    class Meta:
        verbose_name_plural = "geographies"
        ordering = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the available geography as a string.

        :return: The name of the available geography as a string.
        :rtype: str
        """
        return self.name


class SignalGroup(models.Model):
    """
    A model representing a signal group.
    Is a representative group for a small group of signals
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )
    subdivisions = models.ManyToManyField(
        'datasources.SourceSubdivision',
        related_name='signal_groups',
        help_text=_('Source Subdivisions'),
    )
    base = models.ForeignKey(
        'signals.Signal',
        help_text=_('Base Signal'),
        related_name='base_for',
        on_delete=models.PROTECT,
        null=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the signal group as a string.

        :return: The name of the signal group as a string.
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
    pathogen = models.ManyToManyField(
        'signals.Pathogen',
        related_name='signals',
        help_text=_('Pathogen/Disease Area'),
    )
    signal_type = models.ManyToManyField(
        'signals.SignalType',
        related_name='signals',
        help_text=_('Signal Type')
    )
    active = models.BooleanField(
        help_text=_('Active'),
        default=False
    )
    short_description = models.TextField(
        help_text=_('Short Description'),
        max_length=500,
        blank=True
    )
    description = models.TextField(
        help_text=_('Description'),
        max_length=1000,
        blank=True
    )
    format = models.CharField(
        help_text=_('Format'),
        max_length=128,
        choices=FormatChoices.choices
    )
    time_type = models.CharField(
        help_text=_('Time type'),
        max_length=128,
        choices=TimeTypeChoices.choices
    )
    time_label = models.CharField(
        help_text=_('Time label'),
        max_length=128,
        choices=TimeLabelChoices.choices
    )
    category = models.ForeignKey(
        'signals.SignalCategory',
        related_name='signals',
        help_text=_('Signal Category'),
        on_delete=models.SET_NULL,
        null=True
    )
    links = models.ManyToManyField(
        'base.Link',
        help_text=_('Signal links'),
        related_name="signals"
    )
    available_geography = models.ManyToManyField(
        'signals.Geography',
        help_text=_('Available geography')
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
    high_values_are = models.CharField(
        help_text=_('High values are'),
        max_length=128,
        choices=HighValuesAreChoices.choices
    )
    source = models.ForeignKey(
        'datasources.SourceSubdivision',
        related_name='signals',
        help_text=_('Source Subdivision'),
        on_delete=models.PROTECT,
    )
    group = models.ForeignKey(
        'signals.SignalGroup',
        related_name='signals',
        help_text=_('Group'),
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        """
        Returns the name of the signal as a string.

        :return: The name of the signal as a string.
        :rtype: str
        """
        return self.name
