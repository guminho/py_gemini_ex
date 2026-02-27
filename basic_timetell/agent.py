from google.adk.agents.llm_agent import LlmAgent

from tools.tools import get_current_time

root_agent = LlmAgent(
    name="time_agent",
    model="gemini-3-flash-preview",
    description="Tells the current time in a specified city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
