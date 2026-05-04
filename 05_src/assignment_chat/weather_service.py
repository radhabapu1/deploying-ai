import requests
from dotenv import load_dotenv
import os
from langchain.tools import tool

load_dotenv('../.secrets')

@tool
def get_weather(city):
    """ Returns the current weather condition in city of country from weatherstack api"""
    querystring = {
        "access_key": os.getenv("WEATHER_API_KEY"),
        "query": city,
        "units": "m"  # metric (Celsius)
    }
    url = "https://api.weatherstack.com/current"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    return response.json()
    

if __name__ == "__main__":
    print(get_weather("VICTORIA CANADA"))

