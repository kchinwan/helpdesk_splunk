from config.examples import EXAMPLES, REFINEMENT_EXAMPLES
from config.schema_fields import COLUMN_LIST, FIELD_MAPPINGS

def build_prompt(nl_query: str, chat_history: list, extracted_entities: dict = None, preliminary_spl: str = None) -> str:
    """
    Build the prompt to send to Gemini LLM for SPL generation.
    """
    system_prompt = (
        "You are a Splunk chatbot assistant helping analysts write efficient SPL queries.\n"
        "Understand the schema and generate accurate Splunk SPL.\n\n"
        "### Known Schema Fields:\n" + ", ".join(COLUMN_LIST) + 
        "\n\n### Field Mappings:\n" + ", ".join(FIELD_MAPPINGS) + "\n"
    )

    example_prompt = "\n".join([f"User: {ex['user']}\nSPL: {ex['spl']}" for ex in EXAMPLES])

    extracted_str = ""
    if extracted_entities:
        extracted_str += "\nUse the following filters if applicable: "
        extracted_str += ", ".join([f"{k}={v}" for k, v in extracted_entities.items()])

    preliminary_spl_str = ""
    if preliminary_spl:
        preliminary_spl_str = f"Preliminary SPL based on extracted filters:\n{preliminary_spl}\n"

    history_prompt = ""
    if chat_history:
        for entry in chat_history[-3:]:
            history_prompt += f"\nPrevious: {entry['user']}\nSPL: {entry['spl']}"

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


def build_refinement_prompt(existing_spl: str, refinement_instruction: str, extracted_entities: dict = None) -> str:
    """
    Builds a structured prompt for refining an SPL query using Gemini.
    """
    example_prompt = "\n".join([f"User: {ex['user']}\nSPL: {ex['spl']}" for ex in REFINEMENT_EXAMPLES[:3]])

    prompt = (
        "You are a Splunk assistant. Your task is to refine an existing SPL query based on the user's instruction.\n"
        "Only use fields from the known schema. Do not invent new fields.\n\n"
        f"### Known Schema Fields:\n{', '.join(COLUMN_LIST)}\n\n"
        f"### Examples:\n{example_prompt}\n\n"
        f"### Current SPL:\n{existing_spl}\n\n"
    )

    if extracted_entities:
        prompt += "### Extracted Filters (for context):\n"
        for k, v in extracted_entities.items():
            prompt += f"- {k}: {v}\n"
        prompt += "\n"

    prompt += (
        f"### User Instruction:\n{refinement_instruction}\n\n"
        "Please return only the updated SPL query without any explanation or formatting."
    )

    return prompt