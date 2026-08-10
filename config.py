from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_token: str
    groq_model: str
    groq_url: str

    tavily_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
