from django.db import models
from django.utils.translation import gettext_lazy as _
from linkpreview import link_preview


class LinkTypeChoices(models.TextChoices):
    """
    A class representing choices for link types.
    """
    API_DOCUMENTATION = 'api_documentation', _('API Documentation')
    DUA = 'dua', _('DUA')
    INTERPRETING_MASK = 'interpreting_mask', _('Interpreting mask use in context')
    QUESTION_TEXT = 'question_text', _('Question text')
    SURVEY_DETAILS = 'survey_details', _('Survey details')
    SURVEY_DOCUMENTATION = 'survey_documentation', _('Survey documentation')
    TECHNICAL_DESCRIPTION = 'technical_description', _('Technical description')
    WAVE_10_REVISION = 'wave_10_revision', _('Wave 10 revision updates')
    WAVE_11_REVISION = 'wave_11_revision', _('Wave 11 revision updates')
    OTHER = 'other', _('Other')


class Link(models.Model):
    """
    A model representing a Link.
    """
    link_type = models.CharField(
        help_text=_('Link type'),
        choices=LinkTypeChoices.choices,
        max_length=128
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

    def get_preview(self):
        """
        Returns a preview of the link using the link_preview library.

        :return: A dictionary containing information about the link preview, including title, description, and image.
        :rtype: dict
        """
        return link_preview(self)
