import pytest

from twilio.rest import Client


def test_create_twilio_client():
    account_sid = "TEST_ACCOUNT_SID_VALUE"
    auth_token = "TEST_AUTH_TOKEN_VALUE"
    client = Client(account_sid, auth_token)
    assert (client.account_sid == account_sid
            and client.auth_token == auth_token)


def test_create_twilio_message():
    pass
