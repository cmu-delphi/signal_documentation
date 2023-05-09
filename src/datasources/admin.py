from django.contrib import admin

from datasources.models import DataSource, SourceSubdivision


@admin.register(SourceSubdivision)
class SourceSubdivisionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing source subdivision objects.
    """
    list_display = ('name', 'db_source')
    search_fields = ('name', 'db_source')


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing data source objects.
    """
    list_display = ('name',)
    search_fields = ('name', 'source_subdivision__db_source', 'source_subdivision__name', 'description')
