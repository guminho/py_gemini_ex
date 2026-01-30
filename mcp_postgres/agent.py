import os

from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.genai.types import GenerateContentConfig
from mcp import StdioServerParameters

load_dotenv
POSTGRES_URI = os.environ["POSTGRES_URI"]

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="postgres_agent",
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
        temperature=0.2,
        top_p=0.95,
    ),
)
