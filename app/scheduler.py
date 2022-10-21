from typing import Callable, Any, Dict

from abc import ABC
from dataclasses import dataclass

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from error import InvalidTimeOfDayError


class Scheduler(ABC):

    def schedule_task(self, function: Callable[[None], Any], trigger) -> None:
        '''Schedule a task to run when an event is triggered.'''


@dataclass
class TimeOfDay:
    hour: int
    minute: int
    second: int

    def __post__init__(self):
        if not (0 <= self.hour <= 24
                and 0 <= self.minute <= 60
                and 0 <= self.second <= 60):
            raise InvalidTimeOfDayError(self.hour, self.minute, self.second)

    def to_dict(self) -> Dict[str, str]:
        return {
            "hour": str(self.hour),
            "minute": str(self.minute),
            "second": str(self.second),
        }


class DailyScheduler(Scheduler):

    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def schedule_task(self, function: Callable[[None], Any], trigger_time: TimeOfDay) -> None:
        self.scheduler.add_job(
            function,
            trigger="cron",
            day_of_week="mon-sun",
            **trigger_time.to_dict()
        )

    def shutdown_at_exit(self) -> None:
        atexit.register(lambda: self.scheduler.shutdown())
