# Gemini URLs Context

> Demonstrates how to use Google's Gemini API to analyze and compare content
> from web URLs and PDFs directly without manual downloading or preprocessing.

This project showcases Google Gemini's powerful URL context feature that allows
the AI model to fetch and analyze content from web pages and PDF documents
directly. The examples demonstrate practical use cases like comparing API
pricing between different providers and analyzing technical research papers.

📺 [Watch the Tutorial](https://youtu.be/cY7WOYzrdq0)

## Key Features

- Direct URL content analysis using Gemini's URL context tool
- Compare API pricing between different providers (OpenAI vs Anthropic)
- Analyze and compare technical research papers from arXiv
- Rich markdown output formatting with metadata display
- Asynchronous processing for efficient content fetching

## Tech Stack

- Google GenAI (Gemini 2.5 Flash)
- Python-dotenv
- Rich (for beautiful console output)
- Python

## Getting Started

### Prerequisites

- Python 3.12+
- uv
- Google AI API Key (set in `.env`)

### Installation

1. Clone the repository.
2. Navigate to the project directory: `cd projects/gemini-urls-context`
3. Install dependencies using uv: `uv sync`
4. Create a `.env` file and set your Google AI API key:
   ```bash
   GOOGLE_API_KEY=YOUR_GOOGLE_AI_API_KEY
   ```

### Usage

Run the main script to see the demos:

```bash
uv run main.py
```

The script includes two main examples:

1. **API Pricing Comparison**: Compares pricing between OpenAI and Anthropic APIs
2. **Technical Paper Analysis**: Compares research papers (DeepSeek V3 vs Qwen)

You can modify the URLs in `main.py` to analyze different web pages or PDF documents.

## Examples

### API Pricing Comparison
```python
await compare_pricing()
```
This function fetches and compares pricing information from OpenAI and Anthropic websites.

### PDF Research Paper Analysis
```python
await analyze_pdfs()
```
This function downloads and analyzes technical papers from arXiv, providing detailed comparisons.

## How It Works

The project uses Gemini's `url_context` tool which:
1. Fetches content from the provided URLs
2. Processes web pages and PDF documents
3. Provides the content as context to the AI model
4. Returns analysis with metadata about the fetched content

## Use Cases

- **Research**: Compare multiple research papers or technical documents
- **Market Analysis**: Compare pricing, features, or services across websites
- **Content Analysis**: Analyze blog posts, documentation, or articles
- **Due Diligence**: Review multiple sources of information simultaneously

## Notes

- The URL context feature works with both web pages and PDF documents
- Large documents are automatically processed and chunked appropriately
- Metadata about the fetched content is included in the response
- The tool handles authentication and content extraction automatically