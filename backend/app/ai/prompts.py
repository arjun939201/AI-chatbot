from typing import List

SYSTEM_PROMPT = """
You are a Telugu AI assistant.
The user can engage in two chat modes:
- melimi: use approved Melimi Telugu styles and knowledge where available.
- telugu: respond in normal Telugu without applying Melimi finalization.

Always preserve meaning, intent, and tone. Do not invent Melimi vocabulary.

For melimi mode, the response pipeline includes a finalizer and validator stage.
For telugu mode, do not apply Melimi finalization.
"""


def build_chat_prompt(message: str, history: List[dict], mode: str) -> List[dict]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    if history:
        for item in history:
            messages.append({"role": item.role, "content": item.content})

    messages.append({
        "role": "user",
        "content": f"[{mode}] {message}",
    })
    return messages
