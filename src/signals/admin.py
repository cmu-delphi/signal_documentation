from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from signals.models import (
    Geography,
    Pathogen,
    Signal,
    SignalType,
)
from signals.resources import SignalResource


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


@admin.register(Signal)
class SignalAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing signal objects.
    """
    list_display = ('name',)
    search_fields = ('name', 'description', 'short_description')
    list_filter = (
        'pathogen',
        'available_geography',
        'signal_type',
        'format',
        'is_smoothed',
        'is_weighted',
        'is_cumulative',
        'has_stderr',
        'has_sample_size',
    )
    resource_classes = [SignalResource]
