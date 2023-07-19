import re

from import_export import resources
from import_export.fields import Field, widgets

from base.models import Link, LinkTypeChoices
from datasources.models import (
    DataSource,
    ReferenceSignal,
    SourceSubdivision,
)


class SourceSubdivisionResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Source Subdivision')
    display_name = Field(attribute='display_name', column_name='Source Subdivision')
    description = Field(attribute='description', column_name='Description')
    db_source = Field(attribute='db_source', column_name='DB Source')
    data_source = Field(
        attribute='data_source',
        column_name='Name',
        widget=widgets.ForeignKeyWidget(DataSource, field='name'),
    )
    reference_signal = Field(
        attribute='reference_signal',
        column_name='Reference Signal',
        widget=widgets.ForeignKeyWidget(ReferenceSignal, field='name'),
    )
    links = Field(
        attribute='links',
        column_name='Links',
        widget=widgets.ManyToManyWidget(Link, field='url', separator='|'),
    )

    class Meta:
        model = SourceSubdivision
        fields = ('name', 'display_name', 'description', 'data_source', 'reference_signal', 'links')
        import_id_fields = ['name']
        skip_unchanged = True

    def before_import_row(self, row, **kwargs) -> None:
        """
        Hook called before importing each row. Modifies 'Links' column to include
        any additional links specified in 'DUA' or 'Link' columns.
        """
        self.process_links(row)
        self.process_datasource(row)
        self.process_reference_signal(row)

    def process_links(self, row):
        row['Links'] = ''
        if row['DUA']:
            link, created = Link.objects.get_or_create(url=row['DUA'], link_type=LinkTypeChoices.DUA)
            row['Links'] += row['Links'] + f'|{link.url}'
        if row['Link']:
            pattern = r'\[(.*?)\]\((.*?)\)'
            pattern_match = re.search(pattern, row['Link'])
            link_type_mapping = {choice.label: choice.value for choice in LinkTypeChoices}
            link_type = link_type_mapping[pattern_match.group(1)]
            link_url = pattern_match.group(2)
            link, created = Link.objects.get_or_create(url=link_url, link_type=link_type)
            row['Links'] += row['Links'] + f'|{link.url}'

    def process_datasource(self, row):
        if row['Name']:
            data_source, created = DataSource.objects.get_or_create(
                name=row['Name'],
                defaults={
                    'display_name': row['Name'],
                    'description': row['Description'],
                    'source_license': row['License'],
                }
            )
            links = Link.objects.filter(url__in=row['Links'].split('|')).values_list('id', flat=True)
            data_source.links.add(*links)

    def process_reference_signal(self, row):
        if row['Reference Signal']:
            ReferenceSignal.objects.get_or_create(name=row['Reference Signal'])
