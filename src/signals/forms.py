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
    source = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple()
    )
    time_type = forms.ChoiceField(choices=TimeTypeChoices.choices, widget=forms.CheckboxSelectMultiple())
    geographic_scope = forms.ModelMultipleChoiceField(queryset=GeographicScope.objects.all(), widget=forms.CheckboxSelectMultiple())
    severity_pyramid_rungs = forms.ChoiceField(choices=SeverityPyramidRungsChoices.choices, widget=forms.CheckboxSelectMultiple())

    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    signal_availability_days = forms.IntegerField(required=False)

    class Meta:
        model = Signal
        fields: list[str] = [
            'id',
            'order_by',
            'search',
            'pathogen',
            'active',
            'available_geography',
            'severity_pyramid_rungs',
            'source',
            'time_type',
            'geographic_scope',
            'from_date',
            'to_date',
            'signal_availability_days',
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
        self.fields["available_geography"].queryset = self.fields["available_geography"].queryset.order_by("order_id")
        try:
            self.fields["source"].choices = set(SourceSubdivision.objects.values_list('external_name', 'external_name'))
        except SourceSubdivision.DoesNotExist:
            self.fields["source"].choices = []
        for field_name, field in self.fields.items():
            field.required = False
            field.help_text = ''
            field.label = ''
        self.fields['from_date'].label = _('Available Since')
        self.fields['to_date'].label = _('Available Until')
        self.fields['signal_availability_days'].label = _('Available for at least (days)')
