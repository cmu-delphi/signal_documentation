from django.contrib import admin

from datasources.models import (
    DataSource,
    Geography,
    Pathogen,
    Signal,
    SignalType,
    SourceSubdivision,
)


@admin.register(Geography)
class GeographyAdmin(admin.ModelAdmin):
    """
    Admin interface for managing geography objects.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Pathogen)
class PathogenAdmin(admin.ModelAdmin):
    """
    Admin interface for managing pathogen objects.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SignalType)
class SignalTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal type objects.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SourceSubdivision)
class SourceSubdivisionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing source subdivision objects.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Signal)
class SignalAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal objects.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """
    Admin interface for managing data source objects.
    """
    list_display = ('name', 'db_source')
    search_fields = ('name', 'db_source', 'source_subdivision', 'description')
