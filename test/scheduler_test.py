import pytest

from app.scheduler import TimeOfDay
from app.error import InvalidTimeOfDayError


def test_invalid_time_of_day_error_hour():
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(-1, 0, 30)
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(25, 0, 30)


def test_invalid_time_of_day_error_minute():
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, -30, 30)
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, 61, 30)


def test_invalid_time_of_day_error_second():
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, 0, -59)
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, 0, 63)


def test_time_of_day_innit():
    hour, minute, second = 7, 30, 0
    t = TimeOfDay(hour, minute, second)
    assert (t.hour == hour
            and t.minute == minute
            and t.second == second)
