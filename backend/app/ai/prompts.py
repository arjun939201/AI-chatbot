from typing import List

SYSTEM_PROMPT = """
You are a Telugu AI assistant.

You support two chat modes:
- melimi: apply approved Melimi knowledge refinement where available.
- telugu: reply in standard Telugu without Melimi finalization.

Always preserve meaning, intent, tone, and useful existing Telugu structure.
Do not invent official Melimi vocabulary.
"""


def build_chat_prompt(message: str, history: List[dict], mode: str) -> List[dict]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for item in history:
            messages.append({"role": item.role, "content": item.content})

    messages.append({
        "role": "user",
        "content": f"[mode={mode}] {message}",
    })
    return messages
