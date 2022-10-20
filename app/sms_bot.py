import time
import atexit

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler


def print_current_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


def create_app() -> Flask:
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_current_time, trigger="interval", seconds=30)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    return Flask(__name__)


app = create_app()
app.config['DEBUG'] = False


@app.route("/")
def hello_world():
    return "<p>Hello, this is SMS-Bot!</p>"


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    debug = False

    app.run(host=host, port=port, debug=debug)
