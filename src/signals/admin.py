from typing import Literal

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from signals.models import (
    Geography,
    Pathogen,
    Signal,
    SignalCategory,
    SignalType,
)
from signals.resources import SignalBaseResource, SignalResource


@admin.register(SignalCategory)
class SignalCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing signal category objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name']] = ('name',)


@admin.register(Geography)
class GeographyAdmin(admin.ModelAdmin):
    """
    Admin interface for managing geography objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name']] = ('name',)


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


@admin.register(Signal)
class SignalAdmin(ImportExportModelAdmin):
    """
    Admin interface for managing signal objects.
    """
    list_display: tuple[Literal['name']] = ('name',)
    search_fields: tuple[Literal['name'], Literal['description'], Literal['short_description']]
    search_fields = ('name', 'description', 'short_description')
    list_filter: tuple[Literal['pathogen'], Literal['available_geography'], Literal['signal_type'], Literal['format'],
                       Literal['is_smoothed'], Literal['is_weighted'], Literal['is_cumulative'], Literal['has_stderr'], Literal['has_sample_size']]
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
    resource_classes: list[type] = [SignalResource, SignalBaseResource]
