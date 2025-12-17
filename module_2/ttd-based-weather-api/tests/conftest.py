import pytest
from weather_service.providers import MockWeatherProvider
from weather_service.service import WeatherService


@pytest.fixture
def provider():
    return MockWeatherProvider()


@pytest.fixture
def service(provider):
    return WeatherService(provider=provider, api_key="valid-key")
