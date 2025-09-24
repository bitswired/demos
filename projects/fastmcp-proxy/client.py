import asyncio

from fastmcp import Client

mcp_client = Client("http://localhost:8888/mcp")


async def mcp_list_tools():
    async with mcp_client:
        # Basic server interaction
        await mcp_client.ping()

        # List available operations
        tools = await mcp_client.list_tools()

    for tool in tools:
        print("Tool:", tool.name)


if __name__ == "__main__":
    asyncio.run(mcp_list_tools())
