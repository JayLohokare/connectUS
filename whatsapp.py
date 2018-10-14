import json
from twilio.rest import Client

client = None
with open('twilio.json') as f:
    data = json.load(f)
    account_sid = data['account_sid']
    auth_token = data['auth_token']
    client = Client(account_sid, auth_token)


def send_message(number, message):
    message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',
        to='whatsapp:{}'.format(number)
    )
    print(message.sid)
    return "Success"


def send_messages(numbers, message):
    for number in numbers:
        send_message(number, message)
