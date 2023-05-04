from django.db import models
from django.utils.translation import gettext_lazy as _


class LinkTypeChoices(models.TextChoices):
    """
    A class representing choices for link types.
    """
    API_DOCUMENTATION = 'api_documentation', _('API Documentation')
    DUA = 'dua', _('DUA')
    SURVEY_DETAILS = 'survey_details', _('SURVEY_DETAILS')
    OTHER = 'other', _('Other')


class Link(models.Model):
    """
    A model representing a Link.
    """
    link_type = models.CharField(
        help_text=_('Link type'),
        choices=LinkTypeChoices.choices,
        max_length=128,
        unique=True
    )
    url = models.URLField(
        help_text=_('Link url'),
        max_length=256,
        unique=True
    )

    def __str__(self) -> str:
        """
        Returns the name of the link as a string.

        :return: The name of link as a string.
        :rtype: str
        """
        return self.url
