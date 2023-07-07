import re

from import_export import resources
from import_export.fields import Field, widgets

from base.models import Link, LinkTypeChoices
from datasources.models import DataSource, SourceSubdivision


class DataSourceResource(resources.ModelResource):
    """
    A resource for importing and exporting data sources using the Django ORM.
    """
    name = Field(attribute='name', column_name='Name')
    display_name = Field(attribute='display_name', column_name='Name')
    description = Field(attribute='description', column_name='Description')
    source_license = Field(attribute='source_license', column_name='License')
    links = Field(
        attribute='links',
        column_name='Links',
        widget=widgets.ManyToManyWidget(Link, field='url', separator='|'),
    )
    source_subdivisions = Field(
        attribute='source_subdivisions',
        column_name='Name',
        widget=widgets.ForeignKeyWidget(DataSource, field='name'),
    )

    class Meta:
        model = DataSource
        fields = ('name', 'display_name', 'description', 'source_license', 'links')
        import_id_fields = ['name']

    def before_import_row(self, row, **kwargs):
        """
        Hook called before importing each row. Modifies 'Links' column to include
        any additional links specified in 'DUA' or 'Link' columns.
        """
        self.process_links(row)
        self.process_subdivisions(row)

    def process_subdivisions(self, row):
        if row['Source Subdivision']:
            data_source = DataSource.objects.get(name=row['Name'])
            source_subdivision, created = SourceSubdivision.objects.get_or_create(
                name=row['Source Subdivision'],
                defaults={
                    'display_name': row['Source Subdivision'],
                    'description': row['Description'],
                    'db_source': row['DB Source'],
                    'data_source': data_source
                }
            )

    def process_links(self, row):
        row['Links'] = ''
        if row['DUA']:
            link, created = Link.objects.get_or_create(url=row['DUA'], defaults={'link_type': LinkTypeChoices.DUA})
            row['Links'] += row['Links'] + f'|{link.url}'

        if row['Link']:
            pattern = r'\[(.*?)\]\((.*?)\)'
            pattern_match = re.search(pattern, row['Link'])
            link_type_mapping = {choice.label: choice.value for choice in LinkTypeChoices}
            link_type = link_type_mapping[pattern_match.group(1)]
            link_url = pattern_match.group(2)
            link, created = Link.objects.get_or_create(url=link_url, link_type=link_type)
            row['Links'] += row['Links'] + f'|{link.url}'


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
    links = Field(
        attribute='links',
        column_name='Links',
        widget=widgets.ManyToManyWidget(Link, field='url', separator='|'),
    )

    class Meta:
        model = SourceSubdivision
        fields = ('name', 'display_name', 'description', 'links', 'data_source')
        import_id_fields = ['name']
        skip_unchanged = True

    def before_import_row(self, row, **kwargs) -> None:
        """
        Hook called before importing each row. Modifies 'Links' column to include
        any additional links specified in 'DUA' or 'Link' columns.
        """
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
