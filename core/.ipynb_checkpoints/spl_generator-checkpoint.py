from core.prompt_engine import build_prompt
from core.entity_extraction import extract_all_entities
from core.spl_composer import build_spl_query
from utils.helpers import get_gemini_response
from utils.cleaner import clean_spl_output


def generate_spl_query(nl_query: str, chat_history: list = None) -> dict:
    """
    Generate a Splunk SPL query from a natural language input using Gemini,
    assisted by entity extraction for better filter accuracy.

    Args:
        nl_query (str): User's natural language query.
        chat_history (list, optional): Previous chat messages for context.

    Returns:
        dict: {
            "raw_output": str or None,
            "clean_output": str or None,
            "error": str or None
        }
    """
    try:
        # 1. Extract structured entities (filters) from the NL query
        extracted = extract_all_entities(nl_query)

        # Prepare parameters for SPL composer
        index = extracted.get("index") or "ei_prod_mule_apps"
        field_filters = extracted.get("fields") or {}
        keywords = extracted.get("keywords") or []

        # 2. Build preliminary SPL query from extracted entities
        preliminary_spl = build_spl_query(
            index=index,
            field_filters=field_filters,
            keywords=keywords,
        )

        # 3. Build prompt with NL query, chat history, extracted entities, and preliminary SPL
        prompt = build_prompt(nl_query, chat_history or [], extracted, preliminary_spl)

        # 4. Call Gemini LLM to generate raw SPL
        raw_output = get_gemini_response(prompt)

        # 5. Clean up the raw SPL output
        clean_output = clean_spl_output(raw_output)

        return {
            "raw_output": raw_output,
            "clean_output": clean_output,
            "error": None
        }

    except Exception as e:
        return {
            "raw_output": None,
            "clean_output": None,
            "error": f"Failed to generate SPL: {str(e)}"
        }
