import requests
from typing import Any, Dict

from weather_assistant.config import settings

WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"


def get_weather(location: str) -> Dict[str, Any]:
    """
    Fetches current weather details for a given location using WeatherAPI.

    Args:
        location (str): City or location name

    Returns:
        dict: JSON response containing weather details or {'error': '...'}
    """
    params = {"q": location, "key": settings.WEATHER_API_KEY}

    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
