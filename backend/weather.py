import requests
import json

def get_weather_description(lon: float, lat: float):
    # Open weather api key
    with open('weatherapi_key.txt', 'r') as f:
        weatherapi_key = f.read()

    # Request weather data by coordinate
    surl = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={weatherapi_key}'
    r = requests.get(url=surl)
    weather = json.loads(r.text)

    description = weather.get('weather')[0].get('description')  # sunny, overcast, etc...
    wind_speed = weather.get('wind').get('speed')  # units m/s
    wind_direction = weather.get('wind').get('deg')  # units degrees

    return description, wind_speed, wind_direction
