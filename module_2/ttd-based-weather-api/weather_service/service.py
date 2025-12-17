import logging
from .providers import WeatherProvider
from .exceptions import InvalidAPIKeyError

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, provider: WeatherProvider, api_key: str):
        self.provider = provider
        self.api_key = api_key

    def get_forecast(self, city: str):
        logger.info("Received forecast request for %s", city)

        if self.api_key != "valid-key":
            logger.error("Invalid API key used")
            raise InvalidAPIKeyError("Invalid API key")

        forecast = self.provider.fetch(city)

        logger.info("Returning forecast for %s", city)
        return forecast
