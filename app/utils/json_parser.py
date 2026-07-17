import json
import re


def extract_json(text: str) -> dict:
    """
    Extracts the first valid JSON object from an LLM response.

    Returns an empty dict if parsing fails.
    """

    if not text:
        return {}

    text = text.strip()

    # Remove Markdown code fences if present
    text = re.sub(
        r"^```(?:json)?",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"```$",
        "",
        text,
    )

    text = text.strip()

    # First try parsing the entire response
    try:
        return json.loads(text)
    except Exception:
        pass

    # Otherwise extract the first JSON object
    match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL,
    )

    if not match:
        return {}

    try:
        return json.loads(match.group())
    except Exception:
        return {}