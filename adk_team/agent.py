from google.adk.agents.llm_agent import LlmAgent
from google.adk.apps import App

from tools.tools import get_weather, say_goodbye, say_hello

greeting_agent = LlmAgent(
    model="gemini-3-flash-preview",
    name="greeting_agent",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    tools=[say_hello],
)

farewell_agent = LlmAgent(
    model="gemini-3-flash-preview",
    name="farewell_agent",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    tools=[say_goodbye],
)

agent_team = LlmAgent(
    model="gemini-3-flash-preview",
    name="weather_agent",
    description="Main agent: Handles weather, delegates greetings/farewells, saves report to state.",
    instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
    "Handle only weather requests, greetings, and farewells.",
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_weather_report",
)

app = App(
    name="adk_team",  # same as directory name
    root_agent=agent_team,
)
