# core/spl_composer.py

from typing import Dict, List, Optional

DEFAULT_INDEX = "ei_prod_mule_apps"


def build_spl_query(
    index: Optional[str] = None,
    field_filters: Optional[Dict[str, List[str]]] = None,
    keywords: Optional[List[str]] = None,
) -> str:
    """
    Composes a clean SPL query from structured filters and keywords.

    Args:
        index (Optional[str]): The index to use (default: ei_prod_mule_apps)
        field_filters (Dict[str, List[str]]): Field-to-values mapping, e.g. {"OrderNumber": ["12345"]}
        keywords (List[str]): Unstructured keywords to include as raw search terms

    Returns:
        str: Final SPL query
    """
    parts = []

    # Add index
    parts.append(f'index="{index or DEFAULT_INDEX}"')

    if not field_filters:
        field_filters = {}

    # Handle date/time range filters explicitly
    event_from = field_filters.pop("eventDatetime_from", None)
    event_to = field_filters.pop("eventDatetime_to", None)
    event_exact = field_filters.pop("eventDatetime", None)

    if event_exact:
        parts.append(f'eventDatetime="{event_exact}"')
    else:
        # If both from and to are present, use range filter
        if event_from and event_to:
            parts.append(f'eventDatetime>="{event_from}" eventDatetime<="{event_to}"')
        elif event_from:
            parts.append(f'eventDatetime>="{event_from}"')
        elif event_to:
            parts.append(f'eventDatetime<="{event_to}"')

    # Add field-based filters (other than date/time)
    for field, values in field_filters.items():
        if not values:
            continue
        # Apply OR logic if multiple values
        if len(values) > 1:
            clause = "(" + " OR ".join(f'{field}="{val}"' for val in values) + ")"
            parts.append(clause)
        else:
            parts.append(f'{field}="{values[0]}"')

    # Add freeform keywords
    if keywords:
        for kw in keywords:
            parts.append(f'"{kw}"')

    return " ".join(parts)
