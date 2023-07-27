import re
from urllib.parse import urlparse

from import_export import resources
from import_export.fields import Field, widgets

from base.models import Link, LinkTypeChoices
from datasources.models import SourceSubdivision
from signals.models import (
    Geography,
    Pathogen,
    Signal,
    SignalCategory,
    SignalType,
)


class SignalBaseResource(resources.ModelResource):
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
        fields = ['base']
        import_id_fields = ['name', 'source', 'display_name']

    def before_import_row(self, row, **kwargs):
        """Post-processes each row after importing."""
        self.process_base(row)

    def process_base(self, row):
        """Processes base."""

        if row['Signal BaseName']:
            source = SourceSubdivision.objects.get(name=row['Source Subdivision'])
            base_signal = Signal.objects.get(name=row['Signal BaseName'], source=source)
            row['base'] = base_signal.id


class SignalResource(resources.ModelResource):
    """Resource class for importing and exporting Signal models."""

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
    format = Field(attribute='format', column_name='Format')
    time_type = Field(attribute='time_type', column_name='Time Type')
    time_label = Field(attribute='time_label', column_name='Time Label')
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

    class Meta:
        model = Signal
        fields = [
            'name',
            'display_name',
            'pathogen',
            'signal_type',
            'active',
            'short_description',
            'description',
            'format',
            'time_type',
            'time_label',
            'available_geography',
            'is_smoothed',
            'is_weighted',
            'is_cumulative',
            'has_stderr',
            'has_sample_size',
            'high_values_are',
            'source',
            'links'
        ]
        import_id_fields = ['name', 'source', 'display_name']

    def before_import_row(self, row, **kwargs):
        """Pre-processes each row before importing."""
        self.fix_boolean_fields(row, ['Active', 'Is Smoothed', 'Is Weighted', 'Is Cumulative', 'Has StdErr', 'Has Sample Size'])
        self.process_links(row)
        self.process_pathogen(row)

    def is_url_in_domain(self, url, domain):
        """Checks if a URL belongs to a specific domain."""

        parsed_url = urlparse(url)
        return parsed_url.netloc == domain

    def fix_boolean_fields(self, row, fields: list):
        """Fixes boolean fields."""

        for k in fields:
            if row[k] == 'TRUE':
                row[k] = True
            if row[k] == 'FALSE' or row[k] == '':
                row[k] = False
        return row

    def process_links(self, row):
        """Processes links."""

        row['Links'] = ''
        if row['Link']:
            github_domain = "cmu-delphi.github.io"

            links = row['Link'].split('\n')
            for raw_link in links:
                if self.is_url_in_domain(raw_link, github_domain):
                    link, created = Link.objects.get_or_create(url=raw_link, defaults={'link_type': LinkTypeChoices.API_DOCUMENTATION})
                    if f'|{link.url}' not in row['Links']:
                        row['Links'] += row['Links'] + f'|{link.url}'
                pattern = r'\[(.*?)\]\((.*?)\)'
                pattern_match = re.search(pattern, raw_link)
                if pattern_match:
                    link_type_mapping = {choice.label: choice.value for choice in LinkTypeChoices}
                    link_type = link_type_mapping[pattern_match.group(1)]
                    link_url = pattern_match.group(2)
                    link, created = Link.objects.get_or_create(url=link_url, defaults={'link_type': link_type})
                    if f'|{link.url}' not in row['Links']:
                        row['Links'] += row['Links'] + f'|{link.url}'
        return row

    def process_pathogen(self, row):
        """Processes pathogen."""

        if row['Pathogen/ Disease Area']:
            pathogens = row['Pathogen/ Disease Area'].split(',')
            for pathogen in pathogens:
                Pathogen.objects.get_or_create(name=pathogen.strip())
