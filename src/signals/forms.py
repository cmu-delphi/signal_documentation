from django import forms
from django.utils.translation import gettext_lazy as _

from datasources.models import SourceSubdivision
from signals.models import (
    FormatChoices,
    Pathogen,
    Signal,
    TimeLabelChoices,
)

MULTI_SELECT_TOOLTIP_MESSAGE = _('Hold down “Control”, or “Command” on a Mac, to select more than one.')


class SignalFilterForm(forms.ModelForm):
    """
    A form for filtering signals.
    """
    search = forms.CharField(min_length=3)
    pathogen = forms.ModelChoiceField(queryset=Pathogen.objects.all(), empty_label='---------')
    active = forms.NullBooleanField(initial=None)
    format_type = forms.ChoiceField(choices=[('', '---------')] + FormatChoices.choices)
    source = forms.ModelChoiceField(queryset=SourceSubdivision.objects.all(), empty_label='---------')
    time_label = forms.ChoiceField(choices=[('', '---------')] + TimeLabelChoices.choices, label=_('Temporal Resolution'))

    class Meta:
        model = Signal
        fields: list[str] = [
            'search',
            'pathogen',
            'active',
            'available_geography',
            'category',
            'format_type',
            'signal_type',
            'source',
            'time_label',
        ]

        widgets = {
            'search': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter search term'}),
            'pathogen': forms.Select(attrs={'class': 'form-select'}),
            'active': forms.NullBooleanSelect(attrs={'class': 'form-check mt-3', 'label': "Test <i class='ri-stack-line'></i>"},),
            'available_geography': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'bottom',
            }),
            'signal_type': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'bottom',
            }),
            'category': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'bottom',
            }),
            'format_type': forms.Select(attrs={'class': 'form-control'}),
            'source': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'bottom',
            }),
            'time_label': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form.
        """
        super().__init__(*args, **kwargs)

        # Set required attribute to False and disable helptext for all fields
        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ''
            field.label = False
