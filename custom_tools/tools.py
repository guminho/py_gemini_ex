import datetime
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google.adk.tools import ToolContext


def get_current_time(city: str, iana_timezone: str) -> dict:
    """Returns the current time in a specified city."""

    try:
        tz = ZoneInfo(iana_timezone)
    except ZoneInfoNotFoundError as exc:
        return {"status": "error", "error_message": str(exc)}
    else:
        now = datetime.datetime.now(tz)
        return {"status": "success", "city": city, "time": now.isoformat()}


def get_weather(tool_context: ToolContext, city: str) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    preferred_unit = tool_context.state.get("preferred_temperature_unit", "Celsius")
    city_normalized = city.lower().replace(" ", "")  # Basic normalization

    # Mock weather data (always stored in Celsius internally)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Format temperature based on state preference
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9 / 5) + 32  # Calculate Fahrenheit
            temp_unit = "°F"
        else:  # Default to Celsius
            temp_value = temp_c
            temp_unit = "°C"

        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        tool_context.state["last_city_checked"] = city
        return result

    else:
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        return {"status": "error", "error_message": error_msg}


def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
    else:
        greeting = "Hello there!"
    return greeting


def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    print("--- Tool: say_goodbye called ---")
    return "Goodbye! Have a great day."
