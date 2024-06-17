from typing import Any
import logging

import django_filters
from django.db.models import Q
from django_filters.filters import (
    BaseInFilter,
    CharFilter,
    NumberFilter,
    OrderingFilter,
)
from django_filters.widgets import QueryArrayWidget

from datasources.models import SourceSubdivision
from signals.models import (
    FormatChoices,
    Signal,
    TimeTypeChoices,
    GeographicScope,
    SeverityPyramidRungsChoices,
)


logger = logging.getLogger(__name__)


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class SignalFilter(django_filters.FilterSet):
    """
    FilterSet for the Signal model.
    """

    id = NumberInFilter(
        field_name='id',
        lookup_expr='in',
        widget=QueryArrayWidget
    )
    search = CharFilter(method='filter_search')
    order_by = OrderingFilter(
        fields=(
            ('display_name', 'name'),
            ('source__name', 'source'),
            ('last_updated', 'last_updated'),
        )
    )
    format_type = django_filters.MultipleChoiceFilter(choices=FormatChoices.choices)
    severenity_pyramid_rungs = django_filters.MultipleChoiceFilter(choices=SeverityPyramidRungsChoices.choices)
    source = django_filters.ModelMultipleChoiceFilter(queryset=SourceSubdivision.objects.all(),
                                                      field_name="source_id__external_name",
                                                      to_field_name='external_name')
    time_type = django_filters.MultipleChoiceFilter(choices=TimeTypeChoices.choices)

    def __init__(self, data, *args, **kwargs):
        data = data.copy()
        try:
            data.setdefault('geographic_scope', GeographicScope.objects.get(name='USA').id)
        except GeographicScope.DoesNotExist:
            logger.warning("Default Geographic Scope was not found in the database. Using an empty list.")
        super().__init__(data, *args, **kwargs)

    class Meta:
        model = Signal
        fields: list[str] = [
            'id',
            'search',
            'pathogen',
            'active',
            'available_geography',
            'severenity_pyramid_rungs',
            'category',
            'geographic_scope',
            'source',
            'time_type',
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

        query = queries.pop()

        for item in queries:
            query |= item

        return queryset.filter(query)
