# FastMCP Proxy

> Create HTTP proxies for MCP servers to enable remote access and web-based interactions

This project demonstrates how to use FastMCP to create an HTTP proxy for Model Context Protocol (MCP) servers. By wrapping stdio-based MCP servers with an HTTP interface, you can access MCP tools remotely through web APIs, making them available to web applications, remote clients, and other services.

📺 [Watch the Tutorial](https://youtu.be/E1W1zsLd7AE)

## Key Features

- Proxy stdio-based MCP servers over HTTP
- Full MCP feature support through proxy architecture
- Remote access to MCP tools and resources
- Web-friendly API interface for MCP protocols
- Stateless HTTP mode for scalable deployments

## Tech Stack

- FastMCP
- Python 3.12+
- Uvicorn (ASGI server)
- Loguru (logging)
- Rich (console output)
- OpenAI SDK (for AI integrations)

## Getting Started

### Prerequisites

- Python 3.12+
- uv
- Node.js (for running the filesystem MCP server)

### Installation

1. Clone the repository.
2. Navigate to the project directory: `cd fastmcp-proxy`
3. Install dependencies using uv: `uv sync`

### Usage

1. Start the proxy server:
   ```bash
   uv run server.py
   ```

2. In another terminal, test the client:
   ```bash
   uv run client.py
   ```

The proxy server will be available at `http://localhost:8888/mcp` and will proxy requests to the underlying filesystem MCP server.

## Project Structure

```
fastmcp-proxy/
├── README.md           # Project documentation
├── client.py           # Example MCP client
├── pyproject.toml      # Project dependencies
├── scratch.py          # Additional client examples
├── server.py           # Main proxy server
└── .python-version     # Python version specification
```

## Implementation Details

### Server Architecture

The `server.py` creates a proxy that:

1. **Wraps stdio-based MCP servers**: Uses `StdioTransport` to communicate with traditional MCP servers that expect stdin/stdout communication
2. **Exposes HTTP endpoints**: Converts MCP protocol calls into HTTP API endpoints
3. **Maintains full compatibility**: Preserves all MCP features including tools, resources, and prompts
4. **Runs stateless**: Enables horizontal scaling by running in stateless HTTP mode

```python
def build_mcp_proxy():
    transport = StdioTransport(
        command="npx",
        args=[
            "-y",
            "@modelcontextprotocol/server-filesystem",
            ".",
        ],
    )
    # Create a proxy with full MCP feature support
    proxy = FastMCP.as_proxy(ProxyClient(transport=transport), name="FileSystemProxy")
    return proxy
```

### Client Usage

The `client.py` demonstrates how to interact with the proxied MCP server:

```python
async def mcp_list_tools():
    async with mcp_client:
        # Basic server interaction
        await mcp_client.ping()
        # List available operations
        tools = await mcp_client.list_tools()
    
    for tool in tools:
        print("Tool:", tool.name)
```

## Use Cases

- **Web Applications**: Access MCP tools from JavaScript/TypeScript frontends
- **Remote Development**: Use MCP servers from different machines or containers
- **API Integration**: Integrate MCP capabilities into existing REST API workflows
- **Microservices**: Deploy MCP servers as independent HTTP services
- **Cross-Platform Access**: Access MCP tools from any HTTP-capable client

## Development with Zellij

The project includes a Zellij layout (`demo.zellij`) for efficient development:

```bash
zellij --layout demo.zellij
```

This creates a multi-pane setup with separate areas for:
- Code editing
- Server development
- Client testing

## Advanced Configuration

### Custom MCP Servers

Replace the filesystem server with your own MCP server:

```python
transport = StdioTransport(
    command="your-mcp-server",
    args=["--your", "args"],
)
```

### HTTPS and Production

For production deployments, consider:
- Adding SSL/TLS certificates
- Implementing authentication
- Adding rate limiting
- Monitoring and logging

### Scaling

The stateless HTTP mode enables:
- Load balancing across multiple instances
- Container orchestration (Docker, Kubernetes)
- Serverless deployments

## Contributing

1. Fork the repository.
2. Create your feature branch.
3. Submit a pull request.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Additional Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/modelcontextprotocol)
- [Uvicorn Documentation](https://www.uvicorn.org/)