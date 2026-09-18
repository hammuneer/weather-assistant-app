from weather_assistant.utils.formatting import extract_core_metrics

SAMPLE_PAYLOAD = {
    "location": {
        "name": "Lahore",
        "region": "Punjab",
        "country": "Pakistan",
        "lat": 31.55,
        "lon": 74.34,
        "localtime": "2026-09-18 12:00",
    },
    "current": {
        "temp_c": 33.0,
        "feelslike_c": 36.0,
        "humidity": 40,
        "condition": {"text": "Sunny", "icon": "//cdn.weatherapi.com/icon.png"},
        "last_updated": "2026-09-18 12:00",
        "wind_kph": 10.0,
        "wind_dir": "NE",
        "gust_kph": 15.0,
        "pressure_mb": 1010.0,
        "uv": 6.0,
        "vis_km": 10.0,
        "cloud": 5,
        "dewpoint_c": 18.0,
    },
}


def test_extracts_expected_fields():
    core = extract_core_metrics(SAMPLE_PAYLOAD)

    assert core["name"] == "Lahore"
    assert core["temp_c"] == 33.0
    assert core["condition_text"] == "Sunny"
    assert core["wind_dir"] == "NE"


def test_returns_empty_dict_for_error_payload():
    assert extract_core_metrics({"error": "boom"}) == {}


def test_returns_empty_dict_for_empty_payload():
    assert extract_core_metrics({}) == {}
