# core/spl_refiner.py

import re
from core.spl_composer import build_spl_query

def extract_filters_from_spl(spl: str):
    """
    Parses an SPL string and returns structured filter data.
    """
    index_match = re.search(r'index="([^"]+)"', spl)
    index = index_match.group(1) if index_match else None

    field_filters = {}
    for match in re.finditer(r'(\w+)="([^"]+)"', spl):
        key, val = match.groups()
        if key == "index":
            continue
        field_filters.setdefault(key, []).append(val)

    return index, field_filters

def refine_spl_query(existing_spl: str, new_filters: dict) -> str:
    """
    Refines an existing SPL query by merging new filters intelligently.

    Args:
        existing_spl (str): The original SPL string.
        new_filters (dict): Dictionary of new filters {field: [values]}.

    Returns:
        str: Refined SPL query.
    """
    index, existing_filters = extract_filters_from_spl(existing_spl)

    # Merge new filters
    for key, values in new_filters.items():
        if key in existing_filters:
            # Merge and deduplicate
            existing_filters[key] = list(set(existing_filters[key] + values))
        else:
            existing_filters[key] = values

    return build_spl_query(index=index, field_filters=existing_filters)
