import os

from dotenv import load_dotenv

load_dotenv()

GROQ_TOKEN = os.getenv("GROQ_TOKEN")

GROQ_URL = os.getenv(
    "GROQ_URL",
    "https://api.groq.com/openai/v1/chat/completions"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)
