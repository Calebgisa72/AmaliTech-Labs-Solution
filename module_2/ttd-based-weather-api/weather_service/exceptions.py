class WeatherServiceError(Exception):
    """Base class for weather service errors."""


class InvalidAPIKeyError(WeatherServiceError):
    """Raised when API key is invalid."""


class CityNotFoundError(WeatherServiceError):
    """Raised when city is unknown."""
