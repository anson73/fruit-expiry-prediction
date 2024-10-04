import requests

api_key = "3557ceb5ce7bea3f69f0a02fa88342db" # Need to make secret on GitHub

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15)

def get_temperature(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url).json()
    temperature = kelvin_to_celsius(response["main"]["temp"])

    return temperature

if __name__ == '__main__':
    None
    # Tests: 
    # print(get_temperature("london"))
