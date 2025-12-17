import pytest
from weather_service.exceptions import InvalidAPIKeyError, CityNotFoundError
from weather_service.service import WeatherService


def test_invalid_api_key(provider):
    service = WeatherService(provider, api_key="bad-key")

    with pytest.raises(InvalidAPIKeyError):
        service.get_forecast("Kigali")


def test_city_not_found(service):
    with pytest.raises(CityNotFoundError):
        service.get_forecast("Tokyo")
