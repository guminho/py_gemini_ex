import asyncio

from google import genai
from google.genai._adapters import McpToGenAiToolAdapter
from google.genai.types import AutomaticFunctionCallingConfig as AutoFCConfig
from google.genai.types import Content, Part
from google.genai.types import GenerateContentConfig as GenConfig
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = genai.Client()
MODEL = "gemini-3-flash-preview"
MCP_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@wonderwhy-er/desktop-commander@latest"],
)
ALLOWED_TOOLS = ["list_directory", "start_process"]


async def run():
    async with stdio_client(MCP_PARAMS) as (mcp_read, mcp_write):
        async with ClientSession(mcp_read, mcp_write) as mcp_sess:
            await mcp_sess.initialize()
            tool_res = await mcp_sess.list_tools()
            tool_res.tools = [t for t in tool_res.tools if t.name in ALLOWED_TOOLS]
            tool_adapter = McpToGenAiToolAdapter(mcp_sess, tool_res)

            prompt = "What's linux kernel version?"
            contents = [Content(role="user", parts=[Part(text=prompt)])]

            for _ in range(1):
                response = await client.aio.models.generate_content(
                    model=MODEL,
                    contents=contents,
                    config=GenConfig(
                        tools=tool_adapter.tools,
                        automatic_function_calling=AutoFCConfig(disable=True),
                    ),
                )

                if not response.function_calls:
                    break

                print(f"To call: {[fc.name for fc in response.function_calls]}")
                fr_parts = []
                for fc in response.function_calls:
                    mcp_res = await tool_adapter.call_tool(fc)
                    mcp_part = Part.from_function_response(
                        name=fc.name, response={"result": mcp_res}
                    )
                    fr_parts.append(mcp_part)

                contents.append(response.candidates[0].content)
                contents.append(Content(role="user", parts=fr_parts))

            print(f"{response.function_calls=}")
            print(f"{contents[-1].parts=}")


if __name__ == "__main__":
    asyncio.run(run())
