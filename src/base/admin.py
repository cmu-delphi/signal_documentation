from typing import Literal

from django.contrib import admin

from base.models import (
    DescriptedFilter,
    DescriptedFilterField,
    Link,
    License
)


class DescriptedFilterFieldInline(admin.TabularInline):
    model = DescriptedFilterField
    fields = ('description',)
    extra = 0
    can_create = False


@admin.register(DescriptedFilter)
class DescriptedFilterAdmin(admin.ModelAdmin):
    inlines = [DescriptedFilterFieldInline]


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
    Admin interface for managing link objects.
    """
    list_display: tuple[Literal['url'], Literal['link_type']] = ('url', 'link_type')


@admin.register(License)
class GeographyAdmin(admin.ModelAdmin):
    """
    Admin interface for managing license objects.
    """
    list_display: tuple[Literal['name'], Literal['use_restrictions']] = ('name', 'use_restrictions')
    search_fields: tuple[Literal['name']] = ('name',)
