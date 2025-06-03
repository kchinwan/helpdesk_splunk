# core/prompt_engine.py

from config.examples import EXAMPLES
from config.schema_fields import COLUMN_LIST,FIELD_MAPPINGS


def build_prompt(nl_query: str, chat_history: list, extracted_entities: dict = None, preliminary_spl: str = None) -> str:
    """
    Build the prompt to send to Gemini LLM for SPL generation.

    Args:
        nl_query (str): The current user natural language query.
        chat_history (list): List of previous chat dicts, each with keys 'user' and 'spl'.
        extracted_entities (dict, optional): Structured filters extracted from nl_query.
        preliminary_spl (str, optional): Preliminary SPL generated from extracted entities.

    Returns:
        str: The final prompt string to send to Gemini.
    """
    system_prompt = (
        "You are a Splunk chatbot assistant helping analysts write efficient SPL queries."
        " Understand the schema and generate accurate Splunk SPL."
        "\nKnown schema fields: " + ", ".join(COLUMN_LIST) + 
        "\nField mappings (if needed): " + ", ".join(FIELD_MAPPINGS) + "\n"
    )

    # Few-shot examples
    example_prompt = "\n".join([f"User: {ex['user']}\nSPL: {ex['spl']}" for ex in EXAMPLES])

    # Optional extracted filters section
    extracted_str = ""
    if extracted_entities:
        extracted_str += "\nUse the following filters if applicable: "
        extracted_str += ", ".join([f"{k}={v}" for k, v in extracted_entities.items()])
        
    # 4. Add preliminary SPL if available
    preliminary_spl_str = ""
    if preliminary_spl:
        preliminary_spl_str = f"Preliminary SPL based on extracted filters:\n{preliminary_spl}\n"


    # Chat history for better context (if needed)
    history_prompt = ""
    if chat_history:
        for entry in chat_history[-3:]:  # limit to last 3 for brevity
            history_prompt += f"\nPrevious: {entry['user']}\nSPL: {entry['spl']}"

    # Combine all
    full_prompt = (
        system_prompt
        + example_prompt
        + extracted_str
        + "\n"
        + preliminary_spl_str
        + history_prompt
        + f"\n\nNow generate SPL for: {nl_query}"
    )

    return full_prompt
    
   