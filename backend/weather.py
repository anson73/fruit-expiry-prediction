import requests
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

api_key = "3557ceb5ce7bea3f69f0a02fa88342db" # Need to make secret on GitHub

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15)

def get_temperature(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url).json()
    temperature = kelvin_to_celsius(response["main"]["temp"])

    return temperature

def get_humidity(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url).json()
    humidity = response["main"]["humidity"]

    return humidity

def refrigerator_temperature():
    # Optimum refirgerator temperature is between 0 and 5 celcius
    return 1

def get_current_date(location):
    """
    Get current date based on a location (city). 
    """
    geolocator = Nominatim(user_agent="user")
    location = geolocator.geocode(location)
    tz = TimezoneFinder()
    timezone = tz.timezone_at(lng=location.longitude, lat=location.latitude)

    UTC = pytz.utc
    timezone = pytz.timezone(timezone)
    date = datetime.now(timezone).date()

    return date

if __name__ == '__main__':
    None
    # Tests: 
    # print(get_temperature("london"))
    
    print(get_humidity("sydney"))
