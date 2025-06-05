# core/spl_refiner.py

import re
from core.spl_composer import build_spl_query
from utils.helpers import get_gemini_response        
from core.prompt_engine import build_refinement_prompt


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


def refine_spl_query(existing_spl: str, extracted_entities: dict = None, refinement_prompt: str = None) -> str:
    """
    Refines an existing SPL query either by:
    - Merging new structured filters (if no prompt), or
    - Using Gemini to apply a natural language refinement prompt.

    Args:
        existing_spl (str): The original SPL string.
        extracted_entities (dict): Structured filters to merge (optional).
        refinement_prompt (str): Natural language instruction for refinement (optional).

    Returns:
        str: Refined SPL query.
    """
    if refinement_prompt:
        # Use Gemini to refine the SPL based on natural language

        prompt = build_refinement_prompt(existing_spl, refinement_prompt, extracted_entities)

        response = get_gemini_response(prompt)
        return response

    # Fallback: merge structured filters
    index, existing_filters = extract_filters_from_spl(existing_spl)

    if extracted_entities:
        for key, values in extracted_entities.items():
            if not isinstance(values, list):
                values = [values]
            if key in existing_filters:
                existing_filters[key] = list(set(existing_filters[key] + values))
            else:
                existing_filters[key] = values

    return build_spl_query(index=index, field_filters=existing_filters)
