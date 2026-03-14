import io
from datetime import datetime
from typing import Annotated, Sequence, TypedDict

import requests
from geopy.geocoders import Nominatim
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from PIL import Image as PILImage
from pydantic import BaseModel, Field

# Define tools
geolocator = Nominatim(user_agent="weather-app")


class SearchInput(BaseModel):
    location: str = Field(description="The city and state, e.g., San Francisco")
    date: str = Field(
        description="the forecasting date for when to get the weather format (yyyy-mm-dd)"
    )


@tool("get_weather_forecast", args_schema=SearchInput, return_direct=True)
def get_weather_forecast(location: str, date: str):
    """Retrieves the weather using Open-Meteo API.

    Takes a given location (city) and a date (yyyy-mm-dd).

    Returns:
        A dict with the time and temperature for each hour.
    """
    location = geolocator.geocode(location)
    if location:
        try:
            response = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={location.latitude}&longitude={location.longitude}&hourly=temperature_2m&start_date={date}&end_date={date}"
            )
            data = response.json()
            return dict(zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]))
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Location not found"}


# Augment LLM with tools
tools = [get_weather_forecast]
tools_by_name = {tool.name: tool for tool in tools}
model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,
    max_retries=2,
)
model_with_tools = model.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    number_of_steps: int


def llm_call(state: AgentState, config: RunnableConfig):
    return {
        "messages": [model_with_tools.invoke(state["messages"], config)],
    }


def tool_node(state: AgentState):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


def should_continue(state: AgentState):
    """Decide to call tool or stop"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END


# build
agent_builder = StateGraph(AgentState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

agent_builder.set_entry_point("llm_call")
agent_builder.add_conditional_edges(
    "llm_call", should_continue, {"continue": "tool_node", "end": END}
)
agent_builder.add_edge("tool_node", "llm_call")
agent = agent_builder.compile()

# show
PILImage.open(io.BytesIO(agent.get_graph(xray=True).draw_mermaid_png())).show()

# invoke
inputs = {
    "messages": [("user", f"What is the weather in Berlin on {datetime.today()}?")]
}
for state in agent.stream(inputs, stream_mode="values"):
    last_message = state["messages"][-1]
    last_message.pretty_print()

state["messages"].append(("user", "Would it be warmer in Munich?"))
for state in agent.stream(state, stream_mode="values"):
    last_message = state["messages"][-1]
    last_message.pretty_print()
