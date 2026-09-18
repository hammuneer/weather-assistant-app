import requests

from weather_assistant.services.weather_service import get_weather


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_passes_location_as_a_param_not_a_raw_url_fragment(monkeypatch):
    captured = {}

    def fake_get(url, params=None, timeout=None):
        captured["url"] = url
        captured["params"] = params
        return FakeResponse({"location": {"name": "Bosnia & Herzegovina"}})

    monkeypatch.setattr(requests, "get", fake_get)

    result = get_weather("Bosnia & Herzegovina")

    assert captured["params"]["q"] == "Bosnia & Herzegovina"
    assert result["location"]["name"] == "Bosnia & Herzegovina"


def test_returns_error_dict_on_request_exception(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.exceptions.ConnectionError("no network")

    monkeypatch.setattr(requests, "get", fake_get)

    result = get_weather("Lahore")

    assert "error" in result
