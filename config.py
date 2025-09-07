# weatherbot/config.py
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os 

load_dotenv()


class Settings(BaseSettings):
    # --- API keys ---
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", None)
    OPENAI_API_KEY: str  = os.getenv("OPENAI_API_KEY", None)

    # --- Agent model config (used only if OPENAI_API_KEY is set) ---
    OPENAI_MODEL: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.5
    MAX_TOKENS: int = 256

    # --- App behavior ---
    DEFAULT_LOCATION: str = "Lahore"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
