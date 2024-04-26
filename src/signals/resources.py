import re
from typing import Any
from urllib.parse import urlparse

from import_export import resources
from import_export.fields import Field, widgets

from base.models import Link, LinkTypeChoices
from datasources.models import SourceSubdivision
from signals.models import (
    DemographicScope,
    Geography,
    Pathogen,
    Signal,
    SignalCategory,
    SignalType,
)


class SignalBaseResource(resources.ModelResource):
    """
    Resource class for importing Signals base.
    """

    name = Field(attribute='name', column_name='Signal')
    display_name = Field(attribute='display_name', column_name='Name')
    base = Field(
        attribute='base',
        column_name='base',
        widget=widgets.ForeignKeyWidget(Signal, field='id'),
    )
    source = Field(
        attribute='source',
        column_name='Source Subdivision',
        widget=widgets.ForeignKeyWidget(SourceSubdivision, field='name'),
    )

    class Meta:
        model = Signal
        fields: list[str] = ['base']
        import_id_fields: list[str] = ['name', 'source', 'display_name']

    def before_import_row(self, row, **kwargs) -> None:
        """Post-processes each row after importing."""
        self.process_base(row)

    def process_base(self, row) -> None:
        """Processes base."""

        if row['Signal BaseName']:
            source: SourceSubdivision = SourceSubdivision.objects.get(name=row['Source Subdivision'])
            base_signal: Signal = Signal.objects.get(name=row['Signal BaseName'], source=source)
            row['base'] = base_signal.id


class SignalResource(resources.ModelResource):
    """
    Resource class for importing and exporting Signal models
    """

    name = Field(attribute='name', column_name='Signal')
    display_name = Field(attribute='display_name', column_name='Name')
    pathogen = Field(
        attribute='pathogen',
        column_name='Pathogen/ Disease Area',
        widget=widgets.ManyToManyWidget(Pathogen, field='name', separator=','),
    )
    signal_type = Field(
        attribute='signal_type',
        column_name='Signal Type',
        widget=widgets.ManyToManyWidget(SignalType, field='name', separator=','),
    )
    active = Field(attribute='active', column_name='Active')
    short_description = Field(attribute='short_description', column_name='Short Description')
    description = Field(attribute='description', column_name='Description')
    format_type = Field(attribute='format_type', column_name='Format')
    time_type = Field(attribute='time_type', column_name='Time Type')
    time_label = Field(attribute='time_label', column_name='Time Label')
    reporting_cadence = Field(attribute='reporting_cadence', column_name='Reporting Cadence')
    demographic_scope = Field(attribute='demographic_scope', column_name='Demographic Scope')
    severenity_pyramid_rungs = Field(attribute='severenity_pyramid_rungs', column_name='Severity Pyramid Rungs')

    category = Field(
        attribute='category',
        column_name='Category',
        widget=widgets.ForeignKeyWidget(SignalCategory, field='name'),
    )
    available_geography = Field(
        attribute='available_geography',
        column_name='Available Geography',
        widget=widgets.ManyToManyWidget(Geography, field='name', separator=','),
    )
    is_smoothed = Field(attribute='is_smoothed', column_name='Is Smoothed')
    is_weighted = Field(attribute='is_weighted', column_name='Is Weighted')
    is_cumulative = Field(attribute='is_cumulative', column_name='Is Cumulative')
    has_stderr = Field(attribute='has_stderr', column_name='Has StdErr')
    has_sample_size = Field(attribute='has_sample_size', column_name='Has Sample Size')
    high_values_are = Field(attribute='high_values_are', column_name='High Values Are')
    source = Field(
        attribute='source',
        column_name='Source Subdivision',
        widget=widgets.ForeignKeyWidget(SourceSubdivision, field='name'),
    )
    links = Field(
        attribute='links',
        column_name='Links',
        widget=widgets.ManyToManyWidget(Link, field='url', separator='|'),
    )
    data_censoring = Field(attribute='data_censoring', column_name='Data Censoring')
    missingness = Field(attribute='missingness', column_name='Missingness')
    gender_breakdown = Field(attribute='gender_breakdown', column_name='Gender Breakdown')
    race_breakdown = Field(attribute='race_breakdown', column_name='Race Breakdown')
    age_breakdown = Field(attribute='age_breakdown', column_name='Age Breakdown')

    class Meta:
        model = Signal
        fields: list[str] = [
            'name',
            'display_name',
            'pathogen',
            'signal_type',
            'active',
            'short_description',
            'description',
            'format_type',
            'time_type',
            'time_label',
            'reporting_cadence',
            'demographic_scope',
            'severenity_pyramid_rungs',
            'available_geography',
            'is_smoothed',
            'is_weighted',
            'is_cumulative',
            'has_stderr',
            'has_sample_size',
            'high_values_are',
            'source',
            'links',
            'data_censoring',
            'missingness',
            'gender_breakdown',
            'race_breakdown',
            'age_breakdown',
        ]
        import_id_fields: list[str] = ['name', 'source', 'display_name']

    def before_import_row(self, row, **kwargs) -> None:
        """
        Pre-processes each row before importing.
        """

        self.fix_boolean_fields(row, [
            'Active',
            'Is Smoothed',
            'Is Weighted',
            'Is Cumulative',
            'Has StdErr',
            'Has Sample Size',
            'gender_breakdown',
            'race_breakdown',
        ])
        self.process_links(row)
        self.process_pathogen(row)
        self.process_demographic_scope(row)

    def is_url_in_domain(self, url, domain) -> Any:
        """
        Checks if a URL belongs to a specific domain.
        """

        parsed_url: Any = urlparse(url)
        return parsed_url.netloc == domain

    def fix_boolean_fields(self, row, fields: list) -> Any:
        """
        Fixes boolean fields.
        """

        for k in fields:
            if row[k] == 'TRUE':
                row[k] = True
            if row[k] == 'FALSE' or row[k] == '':
                row[k] = False
        return row

    def process_links(self, row) -> Any:
        """
        Processes links.
        """

        row['Links'] = ''
        if row['Link']:
            github_domain = "cmu-delphi.github.io"

            links = row['Link'].split('\n')
            for raw_link in links:
                if self.is_url_in_domain(raw_link, github_domain):
                    link: Link
                    created: bool
                    link, created = Link.objects.get_or_create(url=raw_link, defaults={'link_type': LinkTypeChoices.API_DOCUMENTATION})
                    if f'|{link.url}' not in row['Links']:
                        row['Links'] += row['Links'] + f'|{link.url}'
                pattern = r'\[(.*?)\]\((.*?)\)'
                pattern_match = re.search(pattern, raw_link)
                if pattern_match:
                    link_type_mapping: dict[str, Any] = {choice.label: choice.value for choice in LinkTypeChoices}
                    link_type: str = link_type_mapping[pattern_match.group(1)]
                    link_url: str = pattern_match.group(2)
                    link, created = Link.objects.get_or_create(url=link_url, defaults={'link_type': link_type})
                    if f'|{link.url}' not in row['Links']:
                        row['Links'] += row['Links'] + f'|{link.url}'
        return row

    def process_pathogen(self, row) -> None:
        """
        Processes pathogen.
        """

        if row['Pathogen/ Disease Area']:
            pathogens: str = row['Pathogen/ Disease Area'].split(',')
            for pathogen in pathogens:
                Pathogen.objects.get_or_create(name=pathogen.strip())

    def process_demographic_scope(self, row) -> None:
        """
        Processes demographic scope.
        """

        if row['Demographic Scope']:
            demographic_scopes: str = row['Demographic Scope'].split(',')
            for demographic_scope in demographic_scopes:
                DemographicScope.objects.get_or_create(name=demographic_scope.strip())
