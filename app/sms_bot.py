from functools import partial
import time
from functools import partial

from flask import Flask

from app.scheduler import DailyScheduler, TimeOfDay
from app.tasks.task import weather_report_task

import logging

logging.basicConfig()
logging.getLogger("apscheduler").setLevel(logging.DEBUG)


def print_current_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def create_app() -> Flask:
    app = Flask(__name__)
    app.scheduler = DailyScheduler()
    app.scheduler.shutdown_at_exit()

    app.scheduler.schedule_task(
        partial(weather_report_task, "Brno"), TimeOfDay(15, 30, 0)
    )
    app.scheduler.schedule_task(
        partial(weather_report_task, "Brno"), TimeOfDay(15, 35, 0)
    )
    app.scheduler.schedule_task(
        partial(weather_report_task, "Brno"), TimeOfDay(15, 40, 0)
    )

    return app


app = create_app()
app.config["DEBUG"] = False


@app.route("/")
def index():
    return "<p>Hello, this is SMS-Bot!</p>"

    # List sent messages
    # Show scheduled tasks
    # Process post requests to update tasks


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    debug = False
    app.run(host=host, port=port, debug=debug)
