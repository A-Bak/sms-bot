import pytest

from datetime import datetime

from app.scheduler import DailyScheduler, TimeOfDay
from app.error import InvalidTimeOfDayError


def test_invalid_time_of_day_error_hour():
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(-1, 0, 30)
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(24, 0, 30)


def test_invalid_time_of_day_error_minute():
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, -30, 30)
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, 60, 30)


def test_invalid_time_of_day_error_second():
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, 0, -59)
    with pytest.raises(InvalidTimeOfDayError):
        TimeOfDay(3, 0, 60)


def test_time_of_day_innit():
    hour, minute, second = 7, 30, 0
    t = TimeOfDay(hour, minute, second)
    assert t.hour == hour and t.minute == minute and t.second == second
    

def test_daily_scheduler_schedule_job():
    sch = DailyScheduler()
    job = sch.schedule_task(lambda: None, TimeOfDay(7, 30, 00))
    assert (
        job.next_run_time.hour == 7
        and job.next_run_time.minute == 30
        and job.next_run_time.second == 0
    )
