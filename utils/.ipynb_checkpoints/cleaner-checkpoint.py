# utils/cleaner.py

import re


def clean_spl_output(spl: str) -> str:
    """
    Cleans up Gemini-generated SPL by:
    - Removing unnecessary quotes
    - Normalizing numeric IDs
    - Keeping quoted values only where needed
    """
    # 1. Remove quotes around field names (e.g., "OrderNumber"= → OrderNumber=)
    spl = re.sub(r'"(\w+)"\s*=', r'\1=', spl)

    # 2. Remove quotes around simple alphanumeric values (e.g., OrderNumber="807563904" → OrderNumber=807563904)
    def unquote_id_value(match):
        field = match.group(1)
        val = match.group(2)

        # If value is a number or plain alphanumeric (no spaces or special chars)
        if re.fullmatch(r'[A-Za-z0-9]+', val):
            # For numeric-only values, remove leading zeros (but keep '0')
            if val.isdigit():
                val = val.lstrip('0') or '0'
            return f"{field}={val}"
        else:
            return match.group(0)  # keep quoted if complex

    spl = re.sub(r'(\w+)=["\']([^"\']+)["\']', unquote_id_value, spl)

    # 3. Normalize spacing
    return re.sub(r'\s+', ' ', spl).strip()
