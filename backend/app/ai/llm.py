from typing import List

from backend.app.config import settings
from backend.app.ai.prompts import build_chat_prompt
from backend.app.services.groq_client import GroqClient


groq_client = GroqClient(
    api_key=settings.groq_token,
    model=settings.groq_model,
    url=settings.groq_url,
)


async def generate_chat_response(message: str, history: List[dict], mode: str) -> str:
    prompt_messages = build_chat_prompt(message=message, history=history, mode=mode)
    response = groq_client.generate(messages=prompt_messages)
    return response
