import httplib2
import json
import urllib
import traceback
from twilio.rest import TwilioRestClient

GOOGLE_API_KEY = "AIzaSyC0XYY3AWKWKQlQbwm1mzI0-K4_CoFCCrk"
BASE_URL = "https://www.googleapis.com/language/translate/v2?key=" + GOOGLE_API_KEY

account = "AC29ca8fb35cc8081dc377c648d385b9d0"
token = "5495da193d89b5ebe680ba6e2091a058"


def translate(query, language):
    http = httplib2.Http()
    source = 'en'

    url = BASE_URL + '&q=' + urllib.quote_plus(query) + '&source=' + source + '&target=' + language
    response, body = http.request(url, "GET")
    parsedBody = None

    try:
        if(not response['status'] >= '400'):
            parsedBody = json.loads(body)
        else:
            print("Error from Google's server, no data recieved")
    except json.JSONDecodeError as e:
        print('Couldn\'t decode text')
    except Exception as err:
        print("I don't know what happend. Good luck.", err)
        traceback.print_exc()

    if(parsedBody is not None):
        parsedText = parsedBody['data']['translations'][0]['translatedText']
        return parsedText

    return None


def translateArray(arr, language):
    if(isinstance(arr, list)):
        items = []
        for item in arr:
            if(isinstance(item, list)):
                items.extend(translateArray(item, language))
            elif(isinstance(item, unicode) or isinstance(item, str)):
                items.append(translate(item, language))
        return items
    else:
        assert("Please pass in an array")


def text(number, message):
    if(message is not None):
        client = TwilioRestClient(account, token)
        client.messages.create(to="+1" + number, from_="+19548803086",
                               body=message)
