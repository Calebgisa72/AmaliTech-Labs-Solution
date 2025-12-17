from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherForecast:
    city: str
    temperature_c: float
    description: str
