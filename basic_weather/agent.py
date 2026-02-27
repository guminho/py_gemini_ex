from google.adk.agents import LlmAgent

from tools.tools import get_current_time, get_weather

root_agent = LlmAgent(
    name="weather_time_agent",
    model="gemini-3-flash-preview",
    description="Agent to answer questions about the time and weather in a city.",
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
