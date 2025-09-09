import asyncio

from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig, ToolListUnion
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

client = genai.Client()
model_id = "gemini-2.5-flash"
console = Console()


def render_response(response, title: str, title_color: str = "blue"):
    """Render and display the response with proper markdown formatting."""
    console.print(f"\n[bold {title_color}]{title}[/bold {title_color}]\n", style="bold")

    for each in response.candidates[0].content.parts:
        markdown = Markdown(each.text)
        console.print(markdown)

    console.print(
        f"\n[dim]URL Context Metadata: {response.candidates[0].url_context_metadata}[/dim]"
    )


async def compare_pricing():
    tools: ToolListUnion = [
        {"url_context": {}},
    ]

    url1 = "https://openai.com/api/pricing/"
    url2 = "https://www.anthropic.com/pricing"
    response = await client.aio.models.generate_content(
        model=model_id,
        contents=f"Compare the API pricing between OpenAI {url1} and Anthropic {url2}, group models by category (small vs small, medium vs medium, etc.) and provide a summary of the differences.",
        config=GenerateContentConfig(
            tools=tools,
        ),
    )

    render_response(response, "API Pricing Comparison Report", "blue")


async def analyze_pdfs():
    tools: ToolListUnion = [
        {"url_context": {}},
    ]

    url1 = "https://arxiv.org/pdf/2412.19437"
    url2 = "https://arxiv.org/pdf/2505.09388"

    response = await client.aio.models.generate_content(
        model=model_id,
        contents=f"Compare the technical report of DeepSeek V3 {url1} and Qwene {url2}, and build a report highlighting the key differences.",
        config=GenerateContentConfig(
            tools=tools,
        ),
    )

    render_response(response, "Technical Report Comparison", "green")


asyncio.run(analyze_pdfs())




















