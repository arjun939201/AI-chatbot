import requests
from config import GROQ_TOKEN, GROQ_URL, GROQ_MODEL

SYSTEM_PROMPT = """
You are TelAI.

Always reply in natural Telugu unless the user explicitly requests another language.

Be friendly, conversational, and accurate.
"""

def chat_with_grok(message: str, history=None):
    headers = {
        "Authorization": f"Bearer {GROQ_TOKEN}",
        "Content-Type": "application/json",
    }

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if history:
        for item in history:
            messages.append({
                "role": item["role"],
                "content": item["text"]
            })

    messages.append({
        "role": "user",
        "content": message
    })

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000,
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]