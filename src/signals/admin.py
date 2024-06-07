from typing import Literal

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from signals.models import (
    DemographicScope,
    Geography,
    GeographyUnit,
    Pathogen,
    Signal,
    SignalCategory,
    SignalType,
    GeographySignal,
)
from signals.resources import SignalBaseResource, SignalResource


@admin.register(SignalCategory)
class SignalCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal category objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(GeographyUnit)
class GeographyUnitAdmin(admin.ModelAdmin):
    """
    Admin interface for managing geography unit objects.
    """
    list_display: tuple[Literal['name']] = ('name', 'geo_id', 'geography',)
    search_fields: tuple[Literal['name']] = ('name', 'display_name', 'geo_id',)


@admin.register(Geography)
class GeographyAdmin(admin.ModelAdmin):
    """
    Admin interface for managing geography objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(GeographySignal)
class GeographySignalAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal geography objects.
    """
    list_display: tuple[Literal['geography']] = ('geography', 'signal', 'aggregated_by_delphi')
    search_fields: tuple[Literal['geography']] = ('geography', 'signal', 'aggregated_by_delphi')


@admin.register(Pathogen)
class PathogenAdmin(admin.ModelAdmin):
    """
    Admin interface for managing pathogen objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(SignalType)
class SignalTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal type objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(DemographicScope)
class DemographicScopeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing demographic scope objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(Signal)
class SignalAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing signal objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name'], Literal['description'], Literal['short_description']]
    search_fields = ('name', 'description', 'short_description')
    list_filter = (
        'pathogen',
        'available_geography',
        'signal_type',
        'format_type',
        'time_label',
        'is_smoothed',
        'is_weighted',
        'is_cumulative',
        'has_stderr',
        'has_sample_size',
    )
    resource_classes: list[type] = [SignalResource, SignalBaseResource]
