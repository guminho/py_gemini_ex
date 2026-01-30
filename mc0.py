import asyncio

from fastmcp import Client

client = Client("http://localhost:8080/mcp")


async def call_tool():
    async with client:
        result = await client.call_tool("add", {"a": 10, "b": 22})
        print(result)


asyncio.run(call_tool())
