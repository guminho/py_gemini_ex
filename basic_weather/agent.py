from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.models.google_llm import Gemini
from google.adk.planners import BuiltInPlanner
from google.genai.types import GenerateContentConfig, ThinkingConfig

from tools.tools import get_current_time, get_weather

root_agent = LlmAgent(
    name="weather_time_agent",
    model=Gemini(model="gemini-3-flash-preview"),
    description="Agent to answer questions about the time and weather in a city.",
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
    generate_content_config=GenerateContentConfig(
        temperature=1.0,
    ),
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            thinking_level="high",
            include_thoughts=True,
        )
    ),
)

app = App(
    name="weather_time_app",
    root_agent=root_agent,
)
