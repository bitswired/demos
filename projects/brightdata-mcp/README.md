# BrightData MCP

> Connect BrightData's web scraping capabilities to any MCP-compatible AI client through a FastMCP proxy server

This project demonstrates how to create a web scraping AI agent using BrightData's MCP server and FastMCP proxy. Access powerful web scraping tools including search engines, page scraping, Amazon product data, and LinkedIn company profiles through a simple HTTP interface that works with OpenAI's new Responses API and other MCP-compatible clients.

📺 [Watch the Tutorial](https://youtu.be/FRZJVtZsXbI)

## Key Features

- Proxy BrightData's MCP server over HTTP for remote access
- Web scraping tools: search engines, page scraping, Amazon products, LinkedIn profiles  
- OpenAI Responses API integration with MCP tools
- Ngrok tunnel setup for easy external access
- Interactive CLI with multiple demo functions
- Stateless HTTP mode for scalable deployments

## Tech Stack

- FastMCP (HTTP proxy for MCP servers)
- BrightData MCP Server (@brightdata/mcp)
- OpenAI SDK with Responses API
- Ngrok (tunneling for remote access)
- Python 3.12+
- Rich (console formatting)
- Loguru (logging)

## Getting Started

### Prerequisites

- Python 3.12+
- uv
- Node.js (for running BrightData MCP server)
- BrightData API Key
- Ngrok Auth Token (optional, for remote access)

### Installation

1. Clone the repository.
2. Navigate to the project directory: `cd brightdata-mcp`
3. Install dependencies using uv: `uv sync`
4. Set up environment variables:
   ```bash
   export BRIGHTDATA_API_KEY=your_brightdata_api_key
   export NGROK_AUTHTOKEN=your_ngrok_token  # Optional
   export OPENAI_API_KEY=your_openai_api_key
   ```

### Usage

1. Start the proxy server:
   ```bash
   uv run server.py
   ```

2. In another terminal, run the interactive client:
   ```bash
   # List available tools
   uv run client.py list_tools
   
   # Search Google for latest news
   uv run client.py search_google
   
   # Scrape Hacker News
   uv run client.py scrape_page
   
   # Get Amazon product details
   uv run client.py amazon_product
   
   # Get LinkedIn company profile
   uv run client.py linkedin_company
   ```

## Project Structure

```
brightdata-mcp/
├── README.md           # Project documentation
├── client.py           # Interactive MCP client with demos
├── server.py           # FastMCP proxy server with Ngrok
├── scratch.py          # Development testing script
├── pyproject.toml      # Project dependencies
├── demo.zellij         # Zellij development layout
├── ngrok_url.txt       # Generated Ngrok URL storage
└── .python-version     # Python version specification
```

## Implementation Details

### Server Architecture

The `server.py` creates a proxy that:

1. **Wraps BrightData MCP server**: Uses `StdioTransport` to communicate with BrightData's npm package
2. **Exposes HTTP endpoints**: Converts MCP protocol calls into HTTP API endpoints  
3. **Ngrok integration**: Automatically sets up external tunneling for remote access
4. **Environment configuration**: Passes BrightData API credentials and enables pro mode

```python
def build_mcp_proxy():
    transport = StdioTransport(
        command="npx",
        args=["@brightdata/mcp"],
        env={
            "API_TOKEN": brightdata_api_key,
            "PRO_MODE": "true",
        },
    )
    
    proxy = FastMCP.as_proxy(
        ProxyClient(transport=transport), name="BrightData MCP Proxy"
    )
    return proxy
```

### OpenAI Responses Integration

The client demonstrates seamless integration with OpenAI's Responses API:

```python
mcp_openai_config = {
    "type": "mcp",
    "server_label": "testmcp", 
    "server_description": "BrightData MCP Proxy",
    "server_url": server_url,
    "require_approval": "never",
}

resp = await openai_client.responses.create(
    model="gpt-5-mini",
    tools=[mcp_openai_config],
    input="Use the search engine tool to get latest news about npm supply chain attacks"
)
```

## Available Tools

The BrightData MCP server provides several powerful web scraping tools:

- **Search Engine**: Get search results from Google and other search engines
- **Web Scraping**: Extract content from any webpage as structured markdown
- **Amazon Products**: Get detailed product information, reviews, and characteristics
- **LinkedIn Company Profiles**: Extract company information and insights
- **Advanced Scraping**: Professional-grade data extraction capabilities

## Demo Functions

### Search Google
```bash
uv run client.py search_google
```
Searches for the latest news about npm supply chain attacks and returns top 5 results.

### Scrape Hacker News  
```bash
uv run client.py scrape_page
```
Scrapes Hacker News homepage and analyzes current discussions.

### Amazon Product Analysis
```bash
uv run client.py amazon_product
```
Finds iPhone 16 Pro listings on Amazon and analyzes characteristics and reviews.

### LinkedIn Company Research
```bash
uv run client.py linkedin_company
```
Gets detailed company profile information for OpenAI from LinkedIn.

## Development with Zellij

The project includes a Zellij layout for efficient development:

```bash
zellij --layout demo.zellij
```

Creates a multi-pane setup with:
- Code editing pane
- Server development pane  
- Client testing pane

## Use Cases

- **Market Research**: Analyze competitor products and pricing on e-commerce sites
- **Lead Generation**: Extract company information from LinkedIn for business development
- **Content Monitoring**: Track mentions and discussions across web platforms
- **Price Intelligence**: Monitor product prices and reviews across retailers
- **News Aggregation**: Collect and analyze news from multiple sources
- **SEO Research**: Analyze search engine results and competitor content

## Advanced Configuration

### Custom Scraping Targets

Modify the client examples to scrape different websites:

```python
input="Use scrape as markdown to analyze content from: https://your-target-site.com"
```

### Production Deployment

For production use:
- Remove Ngrok and use proper SSL certificates
- Add authentication and rate limiting  
- Implement proper error handling and retries
- Monitor BrightData usage and costs
- Add logging and observability

### Scaling

The stateless HTTP mode enables:
- Load balancing across multiple proxy instances
- Container orchestration (Docker, Kubernetes)
- Serverless deployments with auto-scaling

## Contributing

1. Fork the repository.
2. Create your feature branch.
3. Submit a pull request.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Additional Resources

- [BrightData MCP Documentation](https://www.npmjs.com/package/@brightdata/mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [OpenAI Responses API](https://platform.openai.com/docs/guides/responses)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [BrightData Platform](https://brightdata.com/)