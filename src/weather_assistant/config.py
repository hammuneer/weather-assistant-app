from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # --- API keys ---
    WEATHER_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    # --- Agent model config (used only if OPENAI_API_KEY is set) ---
    OPENAI_MODEL: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.5
    MAX_TOKENS: int = 256

    # --- App behavior ---
    DEFAULT_LOCATION: str = "Lahore"
    DEBUG: bool = False


settings = Settings()
