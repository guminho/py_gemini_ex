from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.models.google_llm import Gemini
from google.adk.planners import BuiltInPlanner
from google.genai import types

from tools.tools import get_current_time, get_weather

root_agent = LlmAgent(
    model=Gemini(model="gemini-3-flash-preview"),
    name="weather_time_agent",
    description="Agent to answer questions about the time and weather in a city.",
    instruction="You are a helpful agent.",
    tools=[get_weather, get_current_time],
    generate_content_config=types.GenerateContentConfig(
        temperature=1.0,
    ),
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            thinking_level="high",
            include_thoughts=True,
        )
    ),
    # planner=PlanReActPlanner(),
    include_contents="default",
)

app = App(
    name="adk_basic",  # same as directory name
    root_agent=root_agent,
)
