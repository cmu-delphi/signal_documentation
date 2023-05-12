from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from solo.models import SingletonModel


class ContactsConfiguration(SingletonModel):
    address = models.CharField(max_length=255, default='Address')

    def __str__(self) -> str:
        return 'Contacts Configuration'


class ContactPhonenumber(models.Model):
    """
    A model representing a Contact phone number.
    """
    phone_number = PhoneNumberField()
    contacts_config = models.ForeignKey(
        'base.ContactsConfiguration',
        related_name='phone_numbers',
        help_text=_('Contacts phone number'),
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """
        Returns the phone number as a string.

        :return: The phone number as a string.
        :rtype: str
        """
        return self.phone_number.__str__()


class ContactEmail(models.Model):
    """
    A model representing a Contact email.
    """
    email = models.EmailField(max_length=128, help_text=_('Contact email'))
    contacts_config = models.ForeignKey(
        'base.ContactsConfiguration',
        related_name='emails',
        help_text=_('Contacts email'),
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        """
        Returns the email as a string.

        :return: The email as a string.
        :rtype: str
        """
        return self.email


class ContactLink(models.Model):
    """
    A model representing a Contact link.
    """
    contacts_config = models.ForeignKey(
        'base.ContactsConfiguration',
        related_name='links',
        help_text=_('Contacts link'),
        on_delete=models.CASCADE
    )
    name = models.CharField(
        help_text=_('Name'),
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
        return f'{self.name} - {self.url}'


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
