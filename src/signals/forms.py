from django import forms
from django.utils.translation import gettext_lazy as _

from datasources.models import SourceSubdivision
from signals.models import (
    ActiveChoices,
    Pathogen,
    Signal,
    TimeTypeChoices,
    GeographicScope,
    SeverityPyramidRungsChoices,
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
    source = forms.ModelMultipleChoiceField(queryset=SourceSubdivision.objects.all(), widget=forms.CheckboxSelectMultiple())
    time_type = forms.ChoiceField(choices=TimeTypeChoices.choices, widget=forms.CheckboxSelectMultiple())
    geographic_scope = forms.ModelMultipleChoiceField(queryset=GeographicScope.objects.all(), widget=forms.CheckboxSelectMultiple())
    severenity_pyramid_rungs = forms.ChoiceField(choices=SeverityPyramidRungsChoices.choices, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Signal
        fields: list[str] = [
            'id',
            'order_by',
            'search',
            'pathogen',
            'active',
            'available_geography',
            'severenity_pyramid_rungs',
            'source',
            'time_type',
            'geographic_scope',
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
            if field_name == "available_geography":
                field.queryset = field.queryset.order_by("order_id")
