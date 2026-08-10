import requests

from config import GROQ_TOKEN, GROQ_URL, GROQ_MODEL


SYSTEM_PROMPT = """
You are TelAI, a helpful and friendly AI assistant.

Answer the user's questions clearly and accurately.

You can communicate in Telugu, English, and other languages.
Reply in the same language the user uses unless they request another language.

Keep responses natural and useful.
For coding questions, provide practical and correct solutions.
"""


def chat_with_grok(message: str, history=None):

    if not GROQ_TOKEN:
        return "AI service is not configured. Please check the GROQ_TOKEN environment variable."

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

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as error:

        print("Groq API error:", error)

        return "Sorry, I couldn't connect to the AI service right now."

    except Exception as error:

        print("Unexpected error:", error)

        return "Something went wrong while generating the response."
