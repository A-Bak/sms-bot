from typing import TypeAlias
from abc import ABC

import requests
from datetime import datetime

from app.error import ConnectionFailedWeatherAPI, LimitExceededWttrInAPI


FormatedMessage: TypeAlias = str

RESPONSE_OK = 200


class WeatherAPI(ABC):
    def get_weather_report(self, location: str) -> FormatedMessage:
        """Returns a full weather report fir a location."""

    def get_temperature(self, location: str) -> float:
        """Returns temperature at a location."""


class OpenWeatherMapAPI(WeatherAPI):
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_weather_report(self, location: str) -> FormatedMessage:
        response = self._get_request(location=location)

        if response.status_code == RESPONSE_OK:
            return self._format_message(response)
        else:
            response.raise_for_status()

    def get_temperature(self, location: str) -> float:
        raise NotImplementedError

    def _get_request(self, location: str) -> requests.Response:
        url = (
            "https://api.openweathermap.org/data/2.5/weather?"
            + "appid="
            + self.api_key
            + "&q="
            + location
            + "&units=metric"
        )
        try:
            return requests.get(url)
        except requests.ConnectionError as e:
            raise ConnectionFailedWeatherAPI(self.__class__, url) from e

    def _format_message(self, response: requests.Response):
        r = response.json()
        return (
            f'{r["name"]}: {datetime.now().time()}\n'
            + f'Desc: {r["weather"][0]["main"]}, {r["weather"][0]["description"]}\n'
            + f'Temp: {r["main"]["temp"]} °C\n'
            + f'Feel: {r["main"]["feels_like"]} °C\n'
            + f'Wind: {r["wind"]["speed"]} km/h\n'
            + f'Humi: {r["main"]["humidity"]} %\n'
            + f'SunS: {datetime.fromtimestamp(r["sys"]["sunset"]).strftime("%X")}\n'
        )


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
        response = self._get_request(location, self.wttr_format)

        if response.status_code == RESPONSE_OK and not response.text.startswith(
            "Unknown location;"
        ):
            return response.text
        else:
            raise LimitExceededWttrInAPI

    def get_temperature(self, location: str) -> float:
        raise NotImplementedError

    def _get_request(self, location: str, wttr_format: str) -> requests.Response:
        url = f"https://wttr.in/{location}?format={self.wttr_format}"
        try:
            return requests.get(url)
        except requests.ConnectionError as e:
            raise ConnectionFailedWeatherAPI(self.__class__, url) from e
