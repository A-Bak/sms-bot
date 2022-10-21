

class InvalidTimeOfDayError(ValueError):
    def __init__(self, hour: int, minute: int, second: int) -> None:
        message = f"Error: Invalid time of day value {hour}:{minute}:{second}."
        super().__init__(message)
