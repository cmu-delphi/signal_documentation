from django.contrib import admin
from solo.admin import SingletonModelAdmin

from base.models import (
    ContactEmail,
    ContactLink,
    ContactPhonenumber,
    ContactsConfiguration,
    Link,
)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
    Admin interface for managing link objects.
    """
    list_display = ('url', 'link_type')
    search_fields = ('url',)


class ContactLinkInline(admin.TabularInline):
    """
    Inline admin interface for managing contacts link objects.
    """
    model = ContactLink
    extra = 0
    fields = ('name', 'url')


class ContactEmailInline(admin.TabularInline):
    """
    Inline admin interface for managing contacts email objects.
    """
    model = ContactEmail
    extra = 0
    fields = ('email',)


class ContactPhonenumberInline(admin.TabularInline):
    """
    Inline admin interface for managing contacts phone numbers objects.
    """
    model = ContactPhonenumber
    extra = 0
    fields = ('phone_number',)


@admin.register(ContactsConfiguration)
class ContactsConfigurationAdmin(SingletonModelAdmin):
    """
    Admin interface for managing contacts config objects.
    """
    inlines = [ContactEmailInline, ContactLinkInline, ContactPhonenumberInline]
