from twilio.rest import TwilioRestClient

account = "AC29ca8fb35cc8081dc377c648d385b9d0"
token = "5495da193d89b5ebe680ba6e2091a058"
client = TwilioRestClient(account, token)

while True:
    message = client.messages.create(to="+19545361522", from_="+19548803086",
                                     body="Hello there!")
