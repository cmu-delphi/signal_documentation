import django_filters
from django.db.models import Q
from django_filters.filters import CharFilter

from signals.models import Signal


class SignalFilter(django_filters.FilterSet):
    search = CharFilter(method='filter_search')

    class Meta:
        model = Signal
        fields = [
            'search',
            'pathogen',
            'available_geography',
            'signal_type',
            'category',
            'format',
            'source',
            'time_label',
        ]

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        queries = [Q((f'{field}__icontains', value)) for field in ['name', 'description', 'short_description']]
        query = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)
