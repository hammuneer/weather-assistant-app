# weatherbot/utils/formatting.py
from typing import Dict, Any

def extract_core_metrics(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pull out the 'important bits' used in the dashboard.
    """
    if not payload or "error" in payload:
        return {}

    loc = payload.get("location", {}) or {}
    cur = payload.get("current", {}) or {}
    cond = (cur.get("condition") or {})

    return {
        "name": loc.get("name"),
        "region": loc.get("region"),
        "country": loc.get("country"),
        "lat": loc.get("lat"),
        "lon": loc.get("lon"),
        "localtime": loc.get("localtime"),
        "temp_c": cur.get("temp_c"),
        "feelslike_c": cur.get("feelslike_c"),
        "humidity": cur.get("humidity"),
        "condition_text": cond.get("text"),
        "icon": cond.get("icon"),
        "last_updated": cur.get("last_updated"),
        "wind_kph": cur.get("wind_kph"),
        "wind_dir": cur.get("wind_dir"),
        "gust_kph": cur.get("gust_kph"),
        "pressure_mb": cur.get("pressure_mb"),
        "uv": cur.get("uv"),
        "vis_km": cur.get("vis_km"),
        "cloud": cur.get("cloud"),
        "dewpoint_c": cur.get("dewpoint_c"),
    }
