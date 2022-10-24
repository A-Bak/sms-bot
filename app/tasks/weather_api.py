from typing import TypeAlias
from abc import ABC

import requests

from app.error import ConnectionFailedWttrInAPI


FormatedMessage: TypeAlias = str


class WeatherAPI(ABC):
    def get_weather_report(self, location: str) -> FormatedMessage:
        """Returns a full weather report fir a location."""

    def get_temperature(self, location: str) -> float:
        """Returns temperature at a location."""


class OpenWeatherMapAPI(WeatherAPI):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_weather_report(self, location: str) -> FormatedMessage:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather?"
            + "appid="
            + self.api_key
            + "&q="
            + location
        )
        return response.json()

    def get_temperature(self, location: str) -> float:
        raise NotImplementedError


class WttrInAPI(WeatherAPI):
    def __init__(self, wttr_format: str = None) -> None:
        if wttr_format is not None:
            self.wttr_format = wttr_format
        else:
            self.wttr_format = (
                "%l: %T\n"
                + "Temp: %c %t\n"
                + "Feel: %f\n"
                + "Wind: %w\n"
                + "Rain: %p/3hr\n"
                + "Humi: %h\n"
                + "SunS: %s\n"
                + "Moon: %m %M"
            )

    def get_weather_report(self, location: str) -> FormatedMessage:
        return self._get_request(location, self.wttr_format).text

    def get_temperature(self, location: str) -> float:
        raise NotImplementedError

    def _get_request(self, location: str, wttr_format: str) -> requests.Response:
        url = f"https://wttr.in/{location}?format={self.wttr_format}"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response

        except requests.ConnectionError as e:
            raise ConnectionFailedWttrInAPI(url) from e
