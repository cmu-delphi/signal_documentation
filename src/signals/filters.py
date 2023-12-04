from typing import Any

import django_filters
from django.db.models import Q
from django_filters.filters import CharFilter, BooleanFilter

from signals.models import Signal


class SignalFilter(django_filters.FilterSet):
    """
    FilterSet for the Signal model.
    """

    search = CharFilter(method='filter_search')

    class Meta:
        model = Signal
        fields: list[str] = [
            'search',
            'pathogen',
            'active',
            'available_geography',
            'signal_type',
            'category',
            'format_type',
            'source',
            'time_label',
        ]

    def filter_search(self, queryset, name, value) -> Any:
        """
        Custom filter method to perform a search on the Signal model.

        Args:
            queryset (QuerySet): The initial queryset.
            name (str): The name of the filter field.
            value (Any): The value to search for.

        Returns:
            QuerySet: The filtered queryset based on the search value.
        """

        if not value:
            return queryset

        if self.data.get("match_substring"):
            queries: list[Q] = [Q((f'{field}__icontains', value)) for field in ['name', 'description', 'short_description']]
        else:
            queries: list[Q] = [Q((f'{field}__iregex', fr"\b{value}\b")) for field in ['name', 'description', 'short_description']]
        query: Q = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)
