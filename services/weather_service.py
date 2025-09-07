# weatherbot/services/weather_service.py
import requests
from typing import Any, Dict
from config import settings

def get_weather(location: str) -> Dict[str, Any]:
    """
    Fetches current weather details for a given location using WeatherAPI.

    Args:
        location (str): City or location name

    Returns:
        dict: JSON response containing weather details or {'error': '...'}
    """
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.weatherapi.com/v1/current.json?q={location}&key={api_key}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
