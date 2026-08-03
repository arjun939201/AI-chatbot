import os

from dotenv import load_dotenv

load_dotenv()

GROQ_TOKEN = os.getenv("GROQ_TOKEN")
GROQ_MODEL = os.getenv("GROQ_MODEL")
GROQ_URL = os.getenv("GROQ_URL")