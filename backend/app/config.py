import os
from dotenv import load_dotenv

load_dotenv()


def get_env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes")


class Settings:
    debug: bool = get_env_bool("DEBUG", False)
    port: int = int(os.getenv("PORT", "5000"))
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://localhost/melimi")
    groq_token: str = os.getenv("GROQ_TOKEN", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    groq_url: str = os.getenv("GROQ_URL", "https://api.groq.com/openai/v1/chat/completions")


settings = Settings()
