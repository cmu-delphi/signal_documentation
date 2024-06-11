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


class ReportingCadence(models.TextChoices):
    """
    A class representing choices for reporting cadences.
    """
    DAILY = 'daily', _('Daily')
    WEEKLY = 'weekly', _('Weekly')


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


class ActiveChoices(models.TextChoices):
    """
    A class representing choices for active signals.
    """
    ACTIVE = True, _('Current Surveillance Only')


class SeverityPyramidRungsChoices(models.TextChoices):
    """
    A class representing choices for severity pyramid rungs.
    """
    POPULATION = 'population', _('Population')
    INFECTED = 'infected', _('Infected')
    SYMPTOMATIC = 'symptomatic', _('Symptomatic')
    OUTPATIENT_VISIT = 'outpatient_visit', _('Outpatient visit')
    ASCERTAINED = 'ascertained', _('Ascertained (case)')
    HOSPITALIZED = 'hospitalized', _('Hospitalized')
    ICU = 'icu', _('ICU')
    DEAD = 'dead', _('Dead')


class AgeBreakdownChoices(models.TextChoices):
    """
    A class representing choices for age breakdown.
    """
    CILDREN = '0-17', '0-17'
    ADULTS = '18-64', '18-64'
    SENIORS = '65+', '65+'


class SignalCategory(TimeStampedModel):
    """
    A model representing a signal category.
    """
    name: models.CharField = models.CharField(
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
        return str(self.name)


class SignalType(TimeStampedModel):
    """
    A model representing a signal type.
    """
    name: models.CharField = models.CharField(
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
        return str(self.name)


class Pathogen(TimeStampedModel):
    """
    A model representing a pathogen.
    """
    name: models.CharField = models.CharField(
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
        return str(self.name)


class Geography(TimeStampedModel):
    """
    A model representing a available geography.
    """
    name: models.CharField = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    display_name: models.CharField = models.CharField(
        help_text=_('Display Name'),
        max_length=128,
        null=True,
        blank=True
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
        return str(self.display_name)


class GeographySignal(models.Model):
    geography = models.ForeignKey('signals.Geography', on_delete=models.CASCADE, related_name='geography_signals')
    signal = models.ForeignKey('signals.Signal', on_delete=models.CASCADE, related_name='geography_signals')
    aggregated_by_delphi = models.BooleanField(default=False)

    class Meta:
        unique_together = ('geography', 'signal')

    @property
    def display_name(self) -> str:
        """
        Returns the display name of the geography signal.

        :return: The display name of the geography signal.
        :rtype: str
        """
        return f'{self.geography.name} (by Delphi)' if self.aggregated_by_delphi else self.geography.name


class GeographyUnit(TimeStampedModel):
    """
    A model representing a geography (geo-level) unit.
    """

    geo_id: models.CharField = models.CharField(
        help_text=_('Geo ID'),
        max_length=128
    )
    name: models.CharField = models.CharField(
        help_text=_('Name'),
        max_length=128
    )
    display_name: models.CharField = models.CharField(
        help_text=_('Display Name'),
        max_length=128
    )
    level: models.IntegerField = models.IntegerField(help_text=_('Level'))

    geography: models.ForeignKey = models.ForeignKey(
        'signals.Geography',
        related_name='geography_units',
        help_text=_('Geography'),
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """
        Returns the name of the geography unit as a string.

        :return: The name of the geography unit as a string.
        :rtype: str
        """
        return str(self.name)


class GeographicScope(TimeStampedModel):
    """
    A model representing a geographic scope.
    """
    name: models.CharField = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the geographic scope as a string.

        :return: The name of the geographic scope as a string.
        :rtype: str
        """
        return str(self.name)


class DemographicScope(TimeStampedModel):
    """
    A model representing a demographic scope.
    """
    name: models.CharField = models.CharField(
        help_text=_('Name'),
        max_length=128,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the demographic scope as a string.

        :return: The name of the demographic scope as a string.
        :rtype: str
        """
        return str(self.name)


class Organisation(TimeStampedModel):
    """
    A model representing an access list.
    """
    organisation_name: models.CharField = models.CharField(
        help_text=_('Organisation Name'),
        max_length=128,
        unique=True
    )


class Signal(TimeStampedModel):
    """
    A model representing a signal.
    """
    name: models.CharField = models.CharField(
        help_text=_('Name'),
        max_length=128,
    )
    display_name: models.CharField = models.CharField(
        help_text=_('Display Name'),
        max_length=128,
    )
    base: models.ForeignKey = models.ForeignKey(
        'signals.Signal',
        related_name='base_for',
        help_text=_('Signal base'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    pathogen: models.ManyToManyField = models.ManyToManyField(
        'signals.Pathogen',
        related_name='signals',
        help_text=_('Pathogen/Disease Area'),
    )
    signal_type: models.ForeignKey = models.ForeignKey(
        'signals.signalType',
        related_name='signals',
        help_text=_('Source Type'),
        on_delete=models.PROTECT,
        null=True
    )
    active: models.BooleanField = models.BooleanField(
        help_text=_('Active'),
        default=False
    )
    short_description: models.TextField = models.TextField(
        help_text=_('Short Description'),
        max_length=500,
        null=True,
        blank=True
    )
    description: models.TextField = models.TextField(
        help_text=_('Description'),
        max_length=1000,
        null=True,
        blank=True
    )
    format_type: models.CharField = models.CharField(
        help_text=_('Format'),
        max_length=128,
        choices=FormatChoices.choices
    )
    time_type: models.CharField = models.CharField(
        help_text=_('Time type'),
        max_length=128,
        choices=TimeTypeChoices.choices
    )
    time_label: models.CharField = models.CharField(
        help_text=_('Time label'),
        max_length=128,
        choices=TimeLabelChoices.choices
    )
    reporting_cadence: models.CharField = models.CharField(
        help_text=_('Reporting Cadence'),
        max_length=128,
        choices=ReportingCadence.choices,
        null=True
    )
    typical_reporting_lag: models.CharField = models.CharField(
        help_text=_('Typical Reporting Lag'),
        max_length=128,
        null=True,
        blank=True
    )
    typical_revision_cadence: models.CharField = models.CharField(
        help_text=_('Typical Revision Cadence'),
        max_length=512,
        null=True,
        blank=True
    )
    demographic_scope: models.ManyToManyField = models.ManyToManyField(
        'signals.DemographicScope',
        help_text=_('Demographic Scope'),
        related_name='signals',
    )
    severenity_pyramid_rungs: models.CharField = models.CharField(
        help_text=_('Severity Pyramid Rungs'),
        max_length=128,
        choices=SeverityPyramidRungsChoices.choices,
        null=True
    )
    category: models.ForeignKey = models.ForeignKey(
        'signals.SignalCategory',
        related_name='signals',
        help_text=_('Signal Category'),
        on_delete=models.SET_NULL,
        null=True
    )
    links: models.ManyToManyField = models.ManyToManyField(
        'base.Link',
        help_text=_('Signal links'),
        related_name="signals"
    )
    geographic_scope: models.ForeignKey = models.ForeignKey(
        'signals.GeographicScope',
        help_text=_('Geographic Scope'),
        on_delete=models.SET_NULL,
        null=True
    )
    available_geography: models.ManyToManyField = models.ManyToManyField(
        'signals.Geography',
        help_text=_('Available geography'),
        through='signals.GeographySignal'
    )
    temporal_scope_start: models.DateField = models.DateField(
        help_text=_('Temporal Scope Start'),
        null=True,
        blank=True
    )
    temporal_scope_start_note = models.TextField(
        help_text=_('Temporal Scope Start Note'),
        null=True,
        blank=True
    )
    temporal_scope_end: models.DateField = models.DateField(
        help_text=_('Temporal Scope End'),
        null=True,
        blank=True
    )
    temporal_scope_end_note = models.TextField(
        help_text=_('Temporal Scope End Note'),
        null=True,
        blank=True
    )
    gender_breakdown: models.BooleanField = models.BooleanField(
        help_text=_('Gender Breakdown'),
        default=False
    )
    race_breakdown: models.BooleanField = models.BooleanField(
        help_text=_('Race Breakdown'),
        default=False,
    )
    age_breakdown: models.CharField = models.CharField(
        help_text=_('Age Breakdown'),
        max_length=128,
        choices=AgeBreakdownChoices.choices,
        null=True,
    )
    is_smoothed: models.BooleanField = models.BooleanField(
        help_text=_('Is Smoothed'),
        default=False
    )
    is_weighted: models.BooleanField = models.BooleanField(
        help_text=_('Is Weighted'),
        default=False
    )
    is_cumulative: models.BooleanField = models.BooleanField(
        help_text=_('Is Cumulative'),
        default=False
    )
    has_stderr: models.BooleanField = models.BooleanField(
        help_text=_('Has StdErr'),
        default=False
    )
    has_sample_size: models.BooleanField = models.BooleanField(
        help_text=_('Has Sample Size'),
        default=False
    )
    high_values_are: models.CharField = models.CharField(
        help_text=_('High values are'),
        max_length=128,
        choices=HighValuesAreChoices.choices
    )
    source: models.ForeignKey = models.ForeignKey(
        'datasources.SourceSubdivision',
        related_name='signals',
        help_text=_('Source Subdivision'),
        on_delete=models.PROTECT,
    )
    data_censoring: models.TextField = models.TextField(
        help_text=_('Data Censoring'),
        null=True,
        blank=True
    )
    missingness: models.TextField = models.TextField(
        help_text=_('Missingness'),
        null=True,
        blank=True
    )
    organisations_access_list: models.ManyToManyField = models.ManyToManyField(
        'signals.Organisation',
        help_text=_('Organisations Access List. Who may access this signal?'),
        related_name='accessed_signals'
    )

    organisations_sharing_list: models.ManyToManyField = models.ManyToManyField(
        'signals.Organisation',
        help_text=_('Organisations Sharing List. Who may be told about this signal?'),
        related_name='shared_signals'
    )

    license: models.ForeignKey = models.ForeignKey(
        'base.License',
        related_name='signals',
        help_text=_('License'),
        on_delete=models.PROTECT,
        null=True
    )

    restrictions: models.TextField = models.TextField(
        help_text=_('Restrictions'),
        null=True,
        blank=True
    )

    last_updated: models.DateField = models.DateField(
        help_text=_('Last Updated'),
        null=True,
        blank=True
    )
    from_date: models.DateField = models.DateField(
        help_text=_('From Date'),
        null=True,
        blank=True
    )
    to_date: models.DateField = models.DateField(
        help_text=_('To Date'),
        null=True,
        blank=True
    )

    temporal_scope_start: models.CharField = models.CharField(
        help_text=_('Temporal Scope Start'),
        null=True,
        blank=True,
        max_length=128
    )
    temporal_scope_end: models.CharField = models.CharField(
        help_text=_('Temporal Scope End'),
        null=True,
        blank=True,
        max_length=128
    )

    @property
    def is_access_public(self) -> bool:
        """
        Returns True if the signal is public, False otherwise.

        :return: True if the signal is public, False otherwise.
        :rtype: bool
        """
        return self.organisations_access_list.count() == 0

    def is_sharing_public(self) -> bool:
        """
        Returns True if the signal is public, False otherwise.

        :return: True if the signal is public, False otherwise.
        :rtype: bool
        """
        return self.organisations_sharing_list.count() == 0

    @property
    def example_url(self) -> str | None:
        """
        Returns the example URL of the signal.

        :return: The example URL of the signal.
        :rtype: str | None
        """
        example_url = self.links.filter(link_type="example_url").first()
        return example_url.url if example_url else None

    @property
    def has_all_demographic_scopes(self) -> bool:
        """
        Returns True if the signal has all demographic scopes, False otherwise.

        :return: True if the signal has all demographic scopes, False otherwise.
        :rtype: bool
        """
        return self.demographic_scope.count() == DemographicScope.objects.count()

    class Meta:
        unique_together = ['name', 'source']
        ordering: list[str] = ["modified"]

    def __str__(self) -> str:
        """
        Returns the name of the signal as a string.

        :return: The name of the signal as a string.
        :rtype: str
        """
        return str(self.name)

    def clean(self) -> None:
        """
        Validate that the signal has a base if any other signals exist.

        Raises:
            ValidationError: If there are other signals and this signal doesn't have a base.
        """
        if Signal.objects.exists() and not self.base:
            raise ValidationError(_("Signal should have base."))
