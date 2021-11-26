import requests
import os
from twilio.rest import Client

OWN_Endpoint = 'https://api.openweathermap.org/data/2.5/onecall'
api_key = '2b124af7e501b5b506a6cd7a806a245e'

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

weather_params = {
    'lat': 45.366580,
    'lon': 41.709140,
    'appid': api_key,
    'exclude': 'current,minutely,daily',
}

will_rain = False

response = requests.get(OWN_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data['hourly'][:12]
for hour_data in weather_slice:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It\'s going to rain today. Remember to bring an ☂️ .",
        from_='+18129682198',
        to='+79187764761'
    )

    print(message.status)
