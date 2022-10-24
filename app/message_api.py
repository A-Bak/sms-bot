from typing import List, Dict, TypeAlias
from abc import ABC

from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance
from twilio.base.exceptions import TwilioRestException

Message: TypeAlias = Dict[str, str]


class PhoneMessageAPI(ABC):
    def send_message(self, from_number: str, to_number: str, message: str) -> Message:
        """Send message through the SMS REST API."""

    def get_sent_messages(self, message_limit: int) -> List[Message]:
        """Return a list of N=message_limit most recently sent SMS messages."""


class TwilioSMSAPI(PhoneMessageAPI):
    def __init__(self, account_sid: str, auth_token: str) -> None:
        self.client = Client(account_sid, auth_token)

    def send_message(
        self, from_number: str, to_number: str, message: str
    ) -> MessageInstance:
        try:
            return self.client.messages.create(
                from_=from_number, to=to_number, body=message
            )
        except TwilioRestException as e:
            print("Error: Failed to send message through Twilio SMS REST API.")
            raise e

    def get_sent_messages(self, message_limit: int = 50) -> List[MessageInstance]:
        return self.client.messages.list(limit=message_limit)


class TwilioWhatsAppAPI(PhoneMessageAPI):
    def __init__(self, account_sid: str, auth_token: str) -> None:
        self.client = Client(account_sid, auth_token)

    def send_message(self, from_number: str, to_number: str, message: str) -> Message:
        try:
            return self.client.messages.create(
                from_=f"whatsapp:{from_number}",
                to=f"whatsapp:{to_number}",
                message=message,
            )
        except TwilioRestException as e:
            print("Error: Failed to send message through Twilio WhatsApp REST API.")
            raise e
