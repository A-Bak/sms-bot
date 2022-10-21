from typing import Callable, Dict, TypeAlias
from abc import ABC

import os
from functools import partial

from dotenv import load_dotenv
from twilio.rest import Client


Response: TypeAlias = Dict[str, str]


class SMSMessageAPI(ABC):

    def send_message(self, from_number: str, to_number: str, message: str) -> Response:
        '''Send message through the SMS REST API.'''


class TwilioSMSAPI(SMSMessageAPI):

    def __init__(self, account_sid: str, auth_token: str) -> None:
        self.client = Client(account_sid, auth_token)

    def send_message(self, from_number: str, to_number: str, message: str) -> Response:
        return self.client.messages.create(
            from_=from_number,
            to=to_number,
            body=message
        )


def main():
    twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
    verified_phone_number = os.environ['VERIFIED_PHONE_NUMBER']

    twilio_api = TwilioSMSAPI(
        os.environ['TWILIO_ACCOUNT_SID'],
        os.environ['TWILIO_AUTH_TOKEN']
    )

    response = twilio_api.send_message(
        twilio_phone_number,
        verified_phone_number,
        "Example message."
    )

    for x in response:
        print(x)


if __name__ == "__main__":
    load_dotenv()
    main()
