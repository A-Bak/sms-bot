import requests


class InvalidTimeOfDayError(ValueError):
    def __init__(self, hour: int, minute: int, second: int) -> None:
        message = f"Error: Invalid time of day value {hour}:{minute}:{second}."
        super().__init__(message)



class ConnectionFailedWeatherAPI(requests.ConnectionError):
    def __init__(self, api: str, url: str) -> None:
        message = f"Error: Failed to connect to {api} url:{url}."
        super().__init__(message)


class LimitExceededWttrInAPI(ConnectionRefusedError):
    def __init__(self) -> None:
        message = "Error: The wttr.in API has reached its allocated response limit."
        super().__init__(message)
