import asyncio

from google import genai
from google.genai.types import AutomaticFunctionCallingConfig as AutoFCConfig
from google.genai.types import GenerateContentConfig as GenConfig
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = genai.Client()
MODEL = "gemini-3-flash-preview"
MCP_PARAMS = StdioServerParameters(
    command="npx",
    args=["-y", "@wonderwhy-er/desktop-commander@latest"],
)


async def run():
    async with stdio_client(MCP_PARAMS) as (mcp_read, mcp_write):
        async with ClientSession(mcp_read, mcp_write) as mcp_sess:
            await mcp_sess.initialize()

            prompt = "What's linux kernel version?"
            response = await client.aio.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=GenConfig(
                    tools=[mcp_sess],
                    # uses the session, will automatically call the tool
                    automatic_function_calling=AutoFCConfig(
                        disable=False,
                        maximum_remote_calls=1,  # skip-summarization
                    ),
                ),
            )
            print(f"{response.function_calls=}")
            print(f"{response.automatic_function_calling_history=}")
            print(f"{response.text=}")


if __name__ == "__main__":
    asyncio.run(run())
