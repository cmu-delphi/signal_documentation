from typing import Any

from base.models import DescriptedFilter
from base.tools import split_class_name


def filters_descriptions(request) -> dict[str, list[dict[str, Any]]]:
    """
    Adds signal filters descriftions to the context.
    """
    descripted_filters = DescriptedFilter.objects.all()

    results: dict[str, dict[dict[str, dict[str, str]]]] = {
        'filters_descriptions': {
                split_class_name(str(df.filter_name))[-1]: df.descriptions
            } for df in descripted_filters
    }
    return results
