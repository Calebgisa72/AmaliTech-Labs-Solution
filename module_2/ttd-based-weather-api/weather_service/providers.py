from abc import ABC, abstractmethod
from .models import WeatherForecast
from .exceptions import CityNotFoundError


class WeatherProvider(ABC):
    """Abstract weather provider."""

    @abstractmethod
    def fetch(self, city: str) -> WeatherForecast:
        raise NotImplementedError


class MockWeatherProvider(WeatherProvider):
    _DATA = {
        "kigali": WeatherForecast("Kigali", 26.0, "Sunny"),
        "nairobi": WeatherForecast("Nairobi", 22.0, "Cloudy"),
    }

    def fetch(self, city: str) -> WeatherForecast:
        city_key = city.lower()
        if city_key not in self._DATA:
            raise CityNotFoundError(f"City not found: {city}")
        return self._DATA[city_key]
