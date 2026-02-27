import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.genai.types import GenerateContentConfig, ThinkingConfig
from mcp import StdioServerParameters

POSTGRES_URI = os.environ["POSTGRES_URI"]
print(f"{POSTGRES_URI=}")

root_agent = LlmAgent(
    name="postgres_agent",
    model="gemini-3-flash-preview",
    instruction=(
        "You are a PostgreSQL database assistant. "
        "Use the provided tools to query, manage, and interact with "
        "the PostgreSQL database. Ask clarifying questions when unsure."
    ),
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=["postgres-mcp", "--access-mode=unrestricted"],
                    env={"DATABASE_URI": POSTGRES_URI},
                ),
                timeout=60,
            ),
        )
    ],
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
