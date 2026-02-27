import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def get_current_time(city: str, iana_timezone: str) -> dict:
    """Returns the current time in a specified city."""

    try:
        tz = ZoneInfo(iana_timezone)
    except ZoneInfoNotFoundError as exc:
        return {"status": "error", "error_message": str(exc)}
    else:
        now = datetime.datetime.now(tz)
        return {"status": "success", "city": city, "time": now.isoformat()}


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city."""

    city_normalized = city.lower().replace(" ", "")  # Basic normalization

    # Mock weather data
    mock_weather_db = {
        "newyork": {
            "status": "success",
            "report": "The weather in New York is sunny with a temperature of 25°C.",
        },
        "london": {
            "status": "success",
            "report": "It's cloudy in London with a temperature of 15°C.",
        },
        "tokyo": {
            "status": "success",
            "report": "Tokyo is experiencing light rain and a temperature of 18°C.",
        },
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have weather information for '{city}'.",
        }
