import asyncio

import httpx
from fastmcp import Client
from loguru import logger
from openai import AsyncClient as OpenAI
from server import get_server_url

server_url = get_server_url()

mcp_client = Client(server_url)


async def mcp_client_list_tools():
    async with mcp_client:
        # Basic server interaction
        await mcp_client.ping()

        # List available operations
        tools = await mcp_client.list_tools()

        for tool in tools:
            print("Tool:", tool.model_dump_json(indent=2))


async def mcp_client_call_weather():
    async with mcp_client:
        # Basic server interaction
        await mcp_client.ping()

        res = await mcp_client.call_tool(
            name="weather_weather_get", arguments={"location": "New York City"}
        )

        print(res)


async def openai_list_tools():
    openai_client = OpenAI(http_client=httpx.AsyncClient(verify=False, timeout=30.0))

    resp = await openai_client.responses.create(
        model="gpt-5-nano",
        tools=[
            {
                "type": "mcp",
                "server_label": "testmcp",
                "server_description": "A simple MCP server wrapping a FastAPI app",
                "server_url": server_url,
                "require_approval": "never",
            },
        ],
        input="What are the tools available to you my man?",
    )

    print(resp.output_text)


async def openai_get_weather():
    openai_client = OpenAI(http_client=httpx.AsyncClient(verify=False, timeout=30.0))

    resp = await openai_client.responses.create(
        model="gpt-5-nano",
        tools=[
            {
                "type": "mcp",
                "server_label": "testmcp",
                "server_description": "A simple MCP server wrapping a FastAPI app",
                "server_url": server_url,
                "require_approval": "never",
            },
        ],
        input="What's the weather like in New York City?",
    )

    print(resp.output_text)


if __name__ == "__main__":
    import sys

    examples = {
        "mcp_list_tools": mcp_client_list_tools,
        "mcp_call_weather": mcp_client_call_weather,
        "openai_list_tools": openai_list_tools,
        "openai_get_weather": openai_get_weather,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in examples:
        logger.info("Usage: python client.py [example]")
        logger.info("Available examples:", ", ".join(examples.keys()))
        sys.exit(1)

    asyncio.run(examples[sys.argv[1]]())
