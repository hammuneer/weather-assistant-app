import logging
from typing import Optional

from agents import Agent, ModelSettings, Runner
from pydantic import BaseModel, Field

from weather_assistant.config import settings

logger = logging.getLogger(__name__)

INSTRUCTIONS = (
    "You are a helpful weather assistant. Given a query, you need to extract the "
    "location and return the location mentioned in the query as a response."
)


class LocationExtractor(BaseModel):
    location: str = Field(description="Location name, extracted from the user query")


def build_agent() -> Agent:
    """Initializes and returns the configured WeatherAgent."""
    return Agent(
        name="WeatherAgent",
        instructions=INSTRUCTIONS,
        model=settings.OPENAI_MODEL,
        model_settings=ModelSettings(
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        ),
        output_type=LocationExtractor,
    )


async def extract_location_async(query: str) -> Optional[str]:
    """
    Extract the location from a query asynchronously.

    Args:
        query (str): User query containing a location mention.

    Returns:
        Optional[str]: Extracted location or None if not found.
    """
    agent = build_agent()
    try:
        result = await Runner.run(agent, query)
        if result and result.final_output:
            return result.final_output.location
    except Exception:
        logger.exception("Failed to extract location for query: %r", query)
    return None
