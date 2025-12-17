import pytest
from weather_service.providers import MockWeatherProvider
from weather_service.exceptions import CityNotFoundError


def test_mock_provider_known_city():
    provider = MockWeatherProvider()
    forecast = provider.fetch("Kigali")

    assert forecast.description == "Sunny"


def test_mock_provider_unknown_city():
    provider = MockWeatherProvider()

    with pytest.raises(CityNotFoundError):
        provider.fetch("Berlin")
