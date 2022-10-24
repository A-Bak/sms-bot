import requests

class InvalidTimeOfDayError(ValueError):
    def __init__(self, hour: int, minute: int, second: int) -> None:
        message = f"Error: Invalid time of day value {hour}:{minute}:{second}."
        super().__init__(message)


class ConnectionFailedWttrInAPI(requests.ConnectionError):
    def __init__(self, url: str) -> None:
        message = f"Error: Failed to connect to wttr.in API url:{url}."
        super().__init__(message)