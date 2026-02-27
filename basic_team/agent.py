from google.adk.agents.llm_agent import LlmAgent

from tools.tools import get_weather

weather_agent = LlmAgent(
    name="weather_agent",
    model="gemini-3-flash-preview",
    description="Provides weather information.",
    instruction="You are a helpful weather assistant. "
    "Use the 'get_weather' tool for city weather requests. "
    "Clearly present successful reports or polite error messages based on the tool's output status.",
    tools=[get_weather],
)
