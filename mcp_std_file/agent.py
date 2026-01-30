import os

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

TARGET_FOLDER = ".."
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="filesystem_assistant_agent",
    instruction="Help the user manage their files. You can list files, read files, etc.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        # IMPORTANT: This MUST be an ABSOLUTE path
                        os.path.abspath(TARGET_FOLDER),
                    ],
                ),
                timeout=5,
            ),
            tool_filter=[
                "list_directory",
                "read_file",
                "read_multiple_files",
                "search_files",
            ],
        )
    ],
)
