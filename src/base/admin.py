from django.contrib import admin

from base.models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
    Admin interface for managing link objects.
    """
    list_display = ('url', 'link_type')
