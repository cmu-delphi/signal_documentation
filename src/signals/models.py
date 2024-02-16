from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from models_extensions.models import TimeStampedModel


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


class SignalCategory(TimeStampedModel):
    """
    A model representing a signal category.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    class Meta:
        ordering: list[str] = ["name"]
        verbose_name_plural: str = "signal categories"

    def __str__(self) -> str:
        """
        Returns the name of the signal category as a string.

        :return: The name of the signal category as a string.
        :rtype: str
        """
        return self.name


class SignalType(TimeStampedModel):
    """
    A model representing a signal type.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    class Meta:
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the signal type as a string.

        :return: The name of the signal type as a string.
        :rtype: str
        """
        return self.name


class Pathogen(TimeStampedModel):
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


class Geography(TimeStampedModel):
    """
    A model representing a available geography.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    class Meta:
        verbose_name_plural: str = "geographies"
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the available geography as a string.

        :return: The name of the available geography as a string.
        :rtype: str
        """
        return self.name


class Signal(TimeStampedModel):
    """
    A model representing a signal.
    """
    name = models.CharField(
        help_text=_('Name'),
        max_length=128,
    )
    display_name = models.CharField(
        help_text=_('Display Name'),
        max_length=128,
    )
    base = models.ForeignKey(
        'signals.Signal',
        related_name='base_for',
        help_text=_('Signal base'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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
        null=True,
        blank=True
    )
    description = models.TextField(
        help_text=_('Description'),
        max_length=1000,
        null=True,
        blank=True
    )
    format_type = models.CharField(
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

    example_url = models.CharField(
        help_text=_('Example URL'),
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ['name', 'source']
        ordering: list[str] = ["modified"]

    def __str__(self) -> str:
        """
        Returns the name of the signal as a string.

        :return: The name of the signal as a string.
        :rtype: str
        """
        return self.name

    def clean(self) -> None:
        """
        Validate that the signal has a base if any other signals exist.

        Raises:
            ValidationError: If there are other signals and this signal doesn't have a base.
        """
        if Signal.objects.exists() and not self.base:
            raise ValidationError(_("Signal should have base."))
