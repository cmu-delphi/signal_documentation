from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from datasources.models import DataSource, SourceSubdivision
from datasources.resources import SourceSubdivisionResource


@admin.register(SourceSubdivision)
class SourceSubdivisionAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing source subdivision objects.
    """
    list_display = ('name', 'db_source')
    search_fields = ('name', 'db_source')
    resource_classes = [SourceSubdivisionResource]


@admin.register(DataSource)
class DataSourceAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing data source objects.
    """
    list_display = ('name',)
    search_fields = ('name', 'source_subdivision__db_source', 'source_subdivision__name', 'description')
