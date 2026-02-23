import asyncio
from datetime import datetime

from google import genai
from google.genai.types import GenerateContentConfig as GenConfig
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

client = genai.Client()

mcp_params = StdioServerParameters(
    command="npx", args=["-y", "@philschmid/weather-mcp"]
)


async def run():
    async with stdio_client(mcp_params) as (mcp_read, mcp_write):
        async with ClientSession(mcp_read, mcp_write) as mcp_sess:
            await mcp_sess.initialize()

            prompt = f"What is the weather in London in {datetime.now().strftime('%Y-%m-%d')}?"
            response = await client.aio.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config=GenConfig(
                    tools=[mcp_sess],
                    # uses the session, will automatically call the tool
                    # Uncomment if you **don't** want the SDK to automatically call the tool
                    # automatic_function_calling=genai.types.AutomaticFunctionCallingConfig(
                    #     disable=True
                    # ),
                ),
            )
            print(response.text)


# Start the asyncio event loop and run the main function
asyncio.run(run())
