import re
from typing import Literal

from django.db.models import QuerySet
from import_export import resources
from import_export.fields import Field, widgets

from base.models import Link, LinkTypeChoices, License
from datasources.models import DataSource, SourceSubdivision


class SourceSubdivisionResource(resources.ModelResource):
    name = Field(attribute='name', column_name='Source Subdivision')
    display_name = Field(attribute='display_name', column_name='Source Subdivision')
    external_name = Field(attribute='external_name', column_name='External Name')
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
        fields: tuple[Literal['name'], Literal['display_name'], Literal['description'],
                      Literal['data_source'], Literal['reference_signal'], Literal['links'], Literal['external_name']]
        fields = ('name', 'display_name', 'description', 'data_source', 'reference_signal', 'links')
        import_id_fields: list[str] = ['name']
        skip_unchanged = True

    def before_import_row(self, row, **kwargs) -> None:
        """
        Hook called before importing each row. Modifies 'Links' column to include
        any additional links specified in 'DUA' or 'Link' columns.
        """
        self.process_links(row)
        self.process_licenses(row)
        self.process_datasource(row)

    def process_links(self, row) -> None:
        row['Links'] = ''
        if row['DUA']:
            link: Link
            created: bool
            link, created = Link.objects.get_or_create(url=row['DUA'], link_type=LinkTypeChoices.DUA)
            row['Links'] += row['Links'] + f'|{link.url}'
        if row['Link']:
            pattern = r'\[(.*?)\]\((.*?)\)'
            pattern_match = re.search(pattern, row['Link'])
            link_type_mapping = {choice.label: choice.value for choice in LinkTypeChoices}
            link_type: str = link_type_mapping[pattern_match.group(1)]  # type: ignore
            link_url: str = pattern_match.group(2)  # type: ignore
            link, created = Link.objects.get_or_create(url=link_url, link_type=link_type)
            row['Links'] += row['Links'] + f'|{link.url}'

    def process_licenses(self, row) -> None:
        if row['License']:
            license: License
            created: bool
            license, created = License.objects.get_or_create(name=row['License'])
            row['License'] = license

    def process_datasource(self, row) -> None:
        if row['Name']:
            data_source: DataSource
            created: bool
            data_source, created = DataSource.objects.get_or_create(
                name=row['Name'],
                defaults={
                    'display_name': row['Name'],
                    'description': row['Description'],
                    'source_license': row['License'],
                }
            )
            links: QuerySet[Link] = Link.objects.filter(url__in=row['Links'].split('|')).values_list('id', flat=True)
            license: License = License.objects.filter(name=row['License']).first()
            data_source.links.add(*links)
            data_source.source_license = license
