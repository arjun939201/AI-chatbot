import requests

from config import GROQ_TOKEN, GROQ_URL, GROQ_MODEL


SYSTEM_PROMPT = """
You are TelAI, a helpful AI assistant.

Answer clearly and accurately.
Reply in the same language the user uses unless they request another language.
"""


def chat_with_grok(message: str, history=None):

    if not GROQ_TOKEN:
        print("ERROR: GROQ_TOKEN is missing")
        return "GROQ_TOKEN is missing on the server."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if history:
        for item in history[-20:]:
            role = item.get("role")
            content = item.get("content")

            if role in ["user", "assistant"] and content:
                messages.append({
                    "role": role,
                    "content": content
                })

    messages.append({
        "role": "user",
        "content": message
    })

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }

    headers = {
        "Authorization": f"Bearer {GROQ_TOKEN}",
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        print("Groq status:", response.status_code)
        print("Groq response:", response.text)

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as error:

        print("GROQ ERROR:", repr(error))

        return f"AI service error ({type(error).__name__}). Check Render logs."

