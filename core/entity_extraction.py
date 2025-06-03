# core/entity_extraction.py

import re
from config.schema_fields import COLUMN_LIST, FIELD_MAPPINGS as FIELD_MAP


def extract_id(text: str) -> dict:
    """
    Extracts common identifiers like Order numbers, IDs, etc.
    Returns field-value pairs (e.g., OrderNumber=..., uniqueId=...)
    """
    patterns = {
        "OrderNumber": r"\bOrder\s*(?:ID\s*)?#?(\d{6,20})\b",
        "uniqueId": r"\b(?:ID|id)[\s#:]*(\d{6,20})\b",
        "BiNumber": r"\b(?:BI|BiNumber)[\s#:]*(\d{6,20})\b"
    }

    extracted = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted[field] = match.group(1).lstrip('0') or '0'

    return extracted


def extract_systems(text: str) -> dict:
    """
    Extracts systems and assigns them as source/target if possible.
    Uses COLUMN_LIST to determine valid system values.
    """
    found = []
    for token in text.split():
        clean_token = re.sub(r'[^a-zA-Z0-9_\-]', '', token).upper()
        if clean_token in COLUMN_LIST:
            found.append(clean_token)

    found = list(dict.fromkeys(found))  # unique preserve order

    if "from" in text.lower() and "to" in text.lower() and len(found) >= 2:
        return {"metadata.source": found[0], "metadata.target": found[1]}
    elif "from" in text.lower() and len(found) == 1:
        return {"metadata.source": found[0]}
    elif "to" in text.lower() and len(found) == 1:
        return {"metadata.target": found[0]}
    elif len(found) == 2:
        return {"metadata.source": found[0], "metadata.target": found[1]}
    elif len(found) == 1:
        return {"metadata.target": found[0]}
    else:
        return {}


def extract_explicit_fields(text: str) -> dict:
    """
    Matches phrases like: interfaceId is SA00057 → metadata.interfaceId=SA00057
    """
    extracted = {}
    for term, field in FIELD_MAP.items():
        pattern = fr'\b{term}\s*(?:is|=)?\s*"?([\w\-\.]+)"?'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            extracted[field] = match.group(1)

    return extracted


def extract_date_ranges(text: str) -> dict:
    """
    Extract date or date ranges (YYYY-MM-DD) from text.
    Returns eventDatetime or eventDatetime_from and eventDatetime_to
    """
    # Simple ISO date regex (expand if needed)
    date_pattern = r'(\d{4}-\d{2}-\d{2})'
    dates = re.findall(date_pattern, text)

    if len(dates) == 1:
        return {"eventDatetime": dates[0]}
    elif len(dates) >= 2:
        # First two dates assumed as from-to
        return {"eventDatetime_from": dates[0], "eventDatetime_to": dates[1]}
    else:
        return {}


def extract_all_entities(text: str) -> dict:
    """
    Combined extractor for IDs, system direction, explicit fields, and date ranges.
    Returns: dict of field → value for SPL filter composition
    """
    entities = {}
    entities.update(extract_id(text))
    entities.update(extract_systems(text))
    entities.update(extract_explicit_fields(text))
    entities.update(extract_date_ranges(text))
    return entities
