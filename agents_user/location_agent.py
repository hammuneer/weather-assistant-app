# weather_agent.py

from typing import Optional
from pydantic import BaseModel, Field
import asyncio

from agents import Agent, Runner, ModelSettings


# ----- Agent Configuration -----

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
        model="gpt-4o-mini",
        model_settings=ModelSettings(
            temperature=0.5,
            max_tokens=256,
        ),
        output_type=LocationExtractor,
    )


# ----- Async Interface -----

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
    except Exception as e:
        print(f"[extract_location_async] Error: {e}")
    return None