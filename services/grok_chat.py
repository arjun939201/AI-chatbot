import requests

from config import GROQ_TOKEN, GROQ_URL, GROQ_MODEL


SYSTEM_PROMPT = """
You are a helpful and intelligent AI assistant.

Answer the user's questions clearly and accurately.

Reply in the same language the user uses unless they ask for another language.

For programming questions, provide practical and correct solutions.

Be concise when a short answer is sufficient and provide detailed
explanations when the user needs them.
"""


def chat_with_grok(message: str, history=None):

    if not GROQ_TOKEN:
        raise RuntimeError(
            "GROQ_TOKEN is not configured"
        )


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


            if role in ("user", "assistant") and content:

                messages.append(
                    {
                        "role": role,
                        "content": content
                    }
                )


    messages.append(
        {
            "role": "user",
            "content": message
        }
    )


    payload = {

        "model": GROQ_MODEL,

        "messages": messages,

        "temperature": 0.7,

        "max_tokens": 2000

    }


    headers = {

        "Authorization":
            f"Bearer {GROQ_TOKEN}",

        "Content-Type":
            "application/json"

    }


    response = requests.post(

        GROQ_URL,

        headers=headers,

        json=payload,

        timeout=60

    )


    if not response.ok:

        print(
            "GROQ STATUS:",
            response.status_code
        )

        print(
            "GROQ RESPONSE:",
            response.text
        )


        raise RuntimeError(

            f"Groq API returned HTTP "
            f"{response.status_code}: "
            f"{response.text}"

        )


    data = response.json()


    return data["choices"][0]["message"]["content"]
