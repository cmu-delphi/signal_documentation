import django_filters

from signals.models import Signal


class SignalFilter(django_filters.FilterSet):
    class Meta:
        model = Signal
        fields = [
            'pathogen',
            'available_geography',
            'signal_type',
            'format',
            'is_smoothed',
            'is_weighted',
            'is_cumulative',
            'has_stderr',
            'has_sample_size',
        ]
