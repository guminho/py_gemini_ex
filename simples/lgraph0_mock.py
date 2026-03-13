import io

from langgraph.graph import END, START, MessagesState, StateGraph
from PIL import Image as PILImage


def mock_llm(state: MessagesState):
    return {"messages": [{"role": "ai", "content": "hello world"}]}


# build
agent_builder = StateGraph(MessagesState)
agent_builder.add_node(mock_llm)
agent_builder.add_edge(START, "mock_llm")
agent_builder.add_edge("mock_llm", END)
agent = agent_builder.compile()

# show
PILImage.open(io.BytesIO(agent.get_graph(xray=True).draw_mermaid_png())).show()

# invoke
msgs = agent.invoke({"messages": [{"role": "user", "content": "hi!"}]})
print(f"{msgs=}")
