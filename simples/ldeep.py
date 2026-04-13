# pip install -qU deepagents
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = init_chat_model("google_genai:gemini-3-flash-preview")
agent = create_deep_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in Tokyo?"}]}
)
for msg in response["messages"]:
    print(msg)
