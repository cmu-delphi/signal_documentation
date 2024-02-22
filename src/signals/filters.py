from typing import Any

import django_filters
from django.db.models import Q
from django_filters.filters import CharFilter, OrderingFilter

from signals.models import Signal


class SignalFilter(django_filters.FilterSet):
    """
    FilterSet for the Signal model.
    """

    search = CharFilter(method='filter_search')
    order_by = OrderingFilter(
        fields=(
            ('name', 'ame'),
            ('source__name', 'source'),
            ('last_updated', 'last_updated'),
        )
    )

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
        search_tokens = value.split()
        queries: list[Q] = []
        for field in ['name', 'description', 'short_description']:
            token_query: list[Q] = []
            for token in search_tokens:
                if '*' in token:
                    left = token.find('*') == 0
                    right = token.rfind('*') == len(token) - 1
                    token = token.replace('*', '')
                    if left and right:
                        token_query.append(Q((f'{field}__icontains', token)))
                        continue
                    if left:
                        token_query.append(Q((f'{field}__iregex', fr'{token}\b')))
                        continue
                    if right:
                        token_query.append(Q((f'{field}__iregex', fr'\b{token}')))
                        continue
                else:
                    token_query.append(Q((f'{field}__iregex', fr"\b{token}\b")))
                    continue
            query: Q = token_query.pop()
            for item in token_query:
                query &= item
            queries.append(query)

        query: Q = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)
