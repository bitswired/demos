import asyncio
import sys

from fastmcp import Client
from openai import AsyncClient as OpenAI
from rich.console import Console
from server import get_server_url

server_url = get_server_url()

mcp_client = Client(server_url)
console = Console()
openai_client = OpenAI()

mcp_openai_config = {
    "type": "mcp",
    "server_label": "testmcp",
    "server_description": "BrightData MCP Proxy",
    "server_url": server_url,
    "require_approval": "never",
}


async def openai_list_tools():
    openai_client = OpenAI()

    resp = await openai_client.responses.create(
        model="gpt-5-nano",
        tools=[
            mcp_openai_config,
        ],
        input="What are the tools available to you my man?",
    )

    print(resp.output_text)


def display_output(output):
    for x in output:
        if x.type == "reasoning":
            continue
        console.print(f"> type: [bold magenta]{x.type}[/]", style="bold")
        if x.type == "mcp_call":
            console.print(f"[cyan]{x.name}[/] [green]{x.arguments}[/]")
            print(x.output[:30])
        if x.type == "reasoning":
            print(x)
        if x.type == "message":
            print(x.content[0].text)
        print("----" * 4)
        print()


async def openai_search_google():
    resp = await openai_client.responses.create(
        model="gpt-5-mini",
        tools=[
            mcp_openai_config,
        ],
        input="Use the search engine tool to get the latest news about npm supply chain attack on google and give me the 5 top results.",
    )

    display_output(resp.output)


async def openai_scrape_page():
    resp = await openai_client.responses.create(
        model="gpt-5-mini",
        tools=[
            mcp_openai_config,
        ],
        input="Use scrape as markdown to tell me what people are taking about on hackernews: https://news.ycombinator.com",
    )

    display_output(resp.output)


async def openai_amazon_product():
    resp = await openai_client.responses.create(
        model="gpt-5-mini",
        tools=[
            mcp_openai_config,
        ],
        input="Use web_data_amazon_product to get me details about iphone 16 pro listing on amazon.com. Breakdown the chracteristics and the reviews. Just analyze the first listing you find.",
    )

    display_output(resp.output)


async def openai_linkedin_company():
    resp = await openai_client.responses.create(
        model="gpt-5-mini",
        tools=[
            mcp_openai_config,
        ],
        input="Use the web_data_linkedin_company_profile tool to get me details about the company OpenAI on linkedin.com",
    )

    display_output(resp.output)


if __name__ == "__main__":
    # Map function names to actual functions
    runners = {
        "list_tools": openai_list_tools,
        "search_google": openai_search_google,
        "scrape_page": openai_scrape_page,
        "amazon_product": openai_amazon_product,
        "linkedin_company": openai_linkedin_company,
    }

    if len(sys.argv) < 2:
        print("Usage: python client.py <function>")
        print("Available functions:", ", ".join(runners.keys()))
        sys.exit(1)

    func_name = sys.argv[1]
    func = runners.get(func_name)
    if not func:
        print(f"Unknown function: {func_name}")
        print("Available functions:", ", ".join(runners.keys()))
        sys.exit(1)

    asyncio.run(func())
