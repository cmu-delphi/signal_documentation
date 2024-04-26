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
    ACTIVE = True, _('Active')
    HISTORICAL = False, _('Historical')


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

    class Meta:
        verbose_name_plural: str = "geographies"
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns the name of the available geography as a string.

        :return: The name of the available geography as a string.
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


class OrganisationsWithAccess(TimeStampedModel):  # TODO: Requirements for this model are not clear. Need to be discussed.
    """
    A model representing an access list.
    """
    organisation_name: models.CharField = models.CharField(
        help_text=_('Organisation Name'),
        max_length=128,
        unique=True
    )


class SharingOrganisation(TimeStampedModel):  # TODO: Requirements for this model are not clear. Need to be discussed.
    """
    A model representing a sharing organisation.
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
    signal_type: models.ManyToManyField = models.ManyToManyField(
        'signals.SignalType',
        related_name='signals',
        help_text=_('Signal Type')
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
        choices=ReportingCadence.choices
    )
    demographic_scope: models.ManyToManyField = models.ManyToManyField(
        'signals.DemographicScope',
        help_text=_('Demographic Scope'),
        related_name='signals',
    )
    severenity_pyramid_rungs: models.CharField = models.CharField(
        help_text=_('Severity Pyramid Rungs'),
        max_length=128,
        choices=SeverityPyramidRungsChoices.choices
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
    available_geography: models.ManyToManyField = models.ManyToManyField(
        'signals.Geography',
        help_text=_('Available geography')
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
    organisations_access_list: models.ManyToManyField = models.ManyToManyField(  # TODO: Requirements for this field are not clear. Need to be discussed.
        'signals.OrganisationsAccess',
        help_text=_('Organisations Access List')
    )

    organisations_sharing_list: models.ManyToManyField = models.ManyToManyField(  # TODO: Requirements for this field are not clear. Need to be discussed.
        'signals.SharingOrganisation',
        help_text=_('Organisations Sharing List')
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

    @property
    def example_url(self) -> str | None:
        """
        Returns the example URL of the signal.
        """
        example_url = self.links.filter(link_type="example_url").first()
        return example_url.url if example_url else None

    @property
    def has_all_demographic_scopes(self) -> bool:
        """
        Returns True if the signal has all demographic scopes, False otherwise.
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
