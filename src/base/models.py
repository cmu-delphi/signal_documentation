from django.db import models
from django.utils.translation import gettext_lazy as _
from linkpreview import LinkPreview, link_preview
from models_extensions.models import TimeStampedModel
from requests.exceptions import HTTPError

from base.tools import get_class_by_name, split_class_name

FILTERS_LIST: list = [
    ('signals.filters.SignalFilter', 'signals.filters.SignalFilter'),
]


class DescriptedFilterField(models.Model):
    """
    A model representing a filter field that is descripted.
    """
    filter: models.ForeignKey = models.ForeignKey(
        'DescriptedFilter',
        on_delete=models.CASCADE,
        related_name='filter_fields'
    )
    filter_field: models.CharField = models.CharField(help_text=_('Filter field'), max_length=256)
    description: models.TextField = models.TextField(help_text=_('Filter field description'), blank=True, null=True)

    class Meta:
        unique_together = ('filter', 'filter_field')

    def __str__(self) -> str:
        """
        Returns the name of the filter and the filter field
        that associated with description.
        """
        return str(self.filter_field)


class DescriptedFilter(models.Model):
    """
    A model representing a filter wich fields are descripted.
    """
    filter_name: models.CharField = models.CharField(max_length=256, unique=True, choices=FILTERS_LIST)

    def __str__(self) -> str:
        """
        Returns the name of the filter and the filter field
        that associated with description.
        """
        return str(self.filter_name)

    def save(self, *args, **kwargs) -> None:
        """
        Saves the filter description.
        """
        super().save(*args, **kwargs)
        if not self.filter_fields.exists():
            filter_class = get_class_by_name(*split_class_name(self.filter_name))
            for field_name, field in filter_class.base_filters.items():
                DescriptedFilterField.objects.create(
                    filter=self,
                    filter_field=field_name
                )
        super().save(*args, **kwargs)

    @property
    def descriptions(self) -> dict:
        """
        Returns a dictionary with filter fields descriptions.
        """
        return {field.filter_field: field.description for field in self.filter_fields.all()}


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
    EXAMPLE_URL = 'example_url', _('Example URL')


class Link(TimeStampedModel):
    """
    A model representing a Link.
    """
    link_type: models.CharField = models.CharField(
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

    def get_preview(self) -> LinkPreview:
        """
        Returns a preview of the link using the link_preview library.

        :return: A dictionary containing information about the link preview, including title, description, and image.
        :rtype: dict
        """
        try:
            return link_preview(self)
        except HTTPError:
            return {
                'description': _('No description available'),
            }


class License(models.Model):
    """
    A model representing a License.
    """
    name: models.CharField = models.CharField(help_text=_('License'), max_length=256, unique=True)
    use_restrictions: models.TextField = models.TextField(help_text=_('Use Restrictions'), blank=True, null=True)

    def __str__(self) -> str:
        """
        Returns the name of the license as a string.

        :return: The name of the license as a string.
        :rtype: str
        """
        return self.name
