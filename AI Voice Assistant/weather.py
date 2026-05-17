import requests

async def get_weather() -> str:
    """
    Fetch the current weather for New York City using Open-Meteo API.
    Converts temperature to Fahrenheit.

    Returns:
        str: A short weather report.
    """
    # Latitude & longitude for New York City
    lat, lon = 40.7128, -74.0060  

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "current_weather" not in data:
            return "Weather data is unavailable."

        weather = data["current_weather"]
        temp_c = weather["temperature"]
        wind = weather["windspeed"]

        # Convert Celsius → Fahrenheit
        temp_f = (temp_c * 9 / 5) + 32  

        return f"The current temperature in New York City is {temp_f:.1f}°F with wind speed {wind} km/h."
    except Exception as e:
        return f"Failed to fetch weather: {e}"


# if __name__ == "__main__":
#     print(get_weather_newyork())