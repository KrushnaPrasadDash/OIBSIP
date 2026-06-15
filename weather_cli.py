import requests
import sys

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(location):
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()
    except requests.exceptions.RequestException:
        print("Could not connect to the weather service. Check your internet connection.")
        return

    if response.status_code != 200:
        if data.get("cod") == "404" or data.get("cod") == 404:
            print("Location not found. Please check the spelling and try again.")
        elif data.get("cod") == 401:
            print("Invalid API key. Please add a valid OpenWeatherMap API key.")
        else:
            print(f"Error: {data.get('message', 'Unknown error occurred')}")
        return

    name = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    weather_main = data["weather"][0]["main"]
    weather_desc = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    print("-" * 40)
    print(f"Weather Report for {name}, {country}")
    print("-" * 40)
    print(f"Condition    : {weather_main} ({weather_desc})")
    print(f"Temperature  : {temp} C")
    print(f"Feels Like   : {feels_like} C")
    print(f"Humidity     : {humidity}%")
    print(f"Pressure     : {pressure} hPa")
    print(f"Wind Speed   : {wind_speed} m/s")
    print("-" * 40)


def main():
    print("===== Simple Weather App =====")

    if API_KEY == "YOUR_API_KEY_HERE":
        print("Note: You need to set your OpenWeatherMap API key in the API_KEY variable.")
        print("Get a free key at https://openweathermap.org/api")
        print()

    while True:
        location = input("Enter city name or ZIP code (or 'exit' to quit): ").strip()

        if location.lower() == "exit":
            print("Goodbye!")
            sys.exit()

        if location == "":
            print("Please enter a valid location.")
            continue

        get_weather(location)
        print()


if __name__ == "__main__":
    main()
