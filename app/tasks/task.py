import os
from dotenv import load_dotenv

from app.tasks.message_api import TwilioSMSAPI
from app.tasks.weather_api import OpenWeatherMapAPI, WttrInAPI
from app.error import ConnectionFailedWeatherAPI, LimitExceededWttrInAPI


def weather_report_task(location: str) -> None:
    load_dotenv()
    try:
        wttr = WttrInAPI()
        message = wttr.get_weather_report(location=location)
    except (ConnectionFailedWeatherAPI, LimitExceededWttrInAPI):
        owm = OpenWeatherMapAPI(api_key=os.environ["OPEN_WEATHER_MAP_API_KEY"])
        message = owm.get_weather_report(location=location)

    client = TwilioSMSAPI(
        account_sid=os.environ["TWILIO_ACCOUNT_SID"],
        auth_token=os.environ["TWILIO_AUTH_TOKEN"],
    )
    client.send_message(
        from_number=os.environ["TWILIO_PHONE_NUMBER"],
        to_number=os.environ["VERIFIED_PHONE_NUMBER"],
        message=message,
    )
