from django import forms
from django.utils.translation import gettext_lazy as _

from datasources.models import SourceSubdivision
from signals.models import (
    ActiveChoices,
    FormatChoices,
    Pathogen,
    Signal,
    TimeTypeChoices,
)


class SignalFilterForm(forms.ModelForm):
    """
    A form for filtering signals.
    """
    id = forms.ModelMultipleChoiceField(queryset=Signal.objects.all(), widget=forms.MultipleHiddenInput)
    order_by = forms.ChoiceField(choices=[
            ('', '---------'),
            ('name', _('Name')),
            ('source__name', _('Source')),
            ('last_updated', _('Last Updated')),
        ],
        required=False,
    )
    search = forms.CharField(min_length=3)
    pathogen = forms.ModelChoiceField(queryset=Pathogen.objects.all(), widget=forms.CheckboxSelectMultiple())
    active = forms.TypedMultipleChoiceField(choices=ActiveChoices.choices, coerce=bool, widget=forms.CheckboxSelectMultiple())
    format_type = forms.ChoiceField(choices=FormatChoices.choices, widget=forms.CheckboxSelectMultiple())
    source = forms.ModelMultipleChoiceField(queryset=SourceSubdivision.objects.all(), widget=forms.CheckboxSelectMultiple())
    time_type = forms.ChoiceField(choices=TimeTypeChoices.choices, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Signal
        fields: list[str] = [
            'id',
            'order_by',
            'search',
            'pathogen',
            'active',
            'available_geography',
            'category',
            'format_type',
            'signal_type',
            'source',
            'time_type',
        ]

        widgets = {
            'order_by': forms.Select(attrs={
                'class': 'form-select',
                'id': 'order_by',
                'aria-label': 'Order by',
            }),
            'search': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter search term')}),
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
        }

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize the form.
        """
        super().__init__(*args, **kwargs)

        # Set required attribute to False and disable helptext for all fields
        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ''
            field.label = ''
