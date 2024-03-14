from django import forms
from django.utils.translation import gettext_lazy as _

from datasources.models import SourceSubdivision
from signals.models import (
    FormatChoices,
    Pathogen,
    Signal,
    TimeLabelChoices,
    ActiveChoices
)

MULTI_SELECT_TOOLTIP_MESSAGE = _('Hold down “Control”, or “Command” on a Mac, to select more than one.')


class SignalFilterForm(forms.ModelForm):
    """
    A form for filtering signals.
    """
    order_by = forms.ChoiceField(choices=[
            ('', '---------'),
            ('name', 'Name'),
            ('source__name', 'Source'),
            ('last_updated', 'Last Updated'),
        ],
        required=False,
    )
    search = forms.CharField(min_length=3)
    pathogen = forms.ModelChoiceField(queryset=Pathogen.objects.all(), widget=forms.CheckboxSelectMultiple(), empty_label='---------')
    active = forms.TypedMultipleChoiceField(choices=ActiveChoices.choices, coerce=bool, widget=forms.CheckboxSelectMultiple())
    format_type = forms.ChoiceField(choices=[('', '---------')] + FormatChoices.choices)
    source = forms.ModelChoiceField(queryset=SourceSubdivision.objects.all(), empty_label='---------')
    time_label = forms.ChoiceField(choices=[('', '---------')] + TimeLabelChoices.choices, label=_('Temporal Resolution'))

    class Meta:
        model = Signal
        fields: list[str] = [
            'order_by',
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
            'order_by': forms.Select(attrs={
                'class': 'form-select',
                'id': 'order_by',
                'aria-label': 'Order by',
            }),
            'search': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter search term'}),
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
            'format_type': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-select',
                'data-bs-toggle': 'tooltip',
                'data-bs-placement': 'bottom',
            }),
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
