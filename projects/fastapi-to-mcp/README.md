# FastAPI to MCP

> Convert any FastAPI application into a Model Context Protocol (MCP) server with automatic tool generation

This project demonstrates how to transform a FastAPI application into an MCP server that can be consumed by AI models. Using FastMCP, your existing REST endpoints automatically become AI-accessible tools without manual conversion or complex configurations.

📺 [Watch the Tutorial](https://youtu.be/s7BRm3DM4eg)

## Key Features

- Automatic conversion of FastAPI endpoints to MCP tools
- Real-time weather data integration via wttr.in API
- Ngrok tunnel for public accessibility
- Direct MCP client integration examples
- OpenAI API integration with MCP tools
- Zero-configuration tool generation

## Tech Stack

- FastAPI
- FastMCP
- MCP (Model Context Protocol)
- OpenAI API
- Ngrok
- httpx
- Loguru

## Getting Started

### Prerequisites

- Python 3.12+
- uv
- Ngrok account and authtoken

### Installation

1. Clone the repository.
2. Navigate to the project directory: `cd projects/fastapi-to-mcp`
3. Install dependencies using uv: `uv sync`
4. Set up your Ngrok authtoken:
   ```bash
   export NGROK_AUTHTOKEN=your_ngrok_authtoken_here
   ```

### Usage

1. Start the MCP server:
   ```bash
   uv run server.py
   ```
   
   This will:
   - Start a FastAPI server on port 8888
   - Create an Ngrok tunnel for public access
   - Convert all FastAPI endpoints to MCP tools
   - Save the public URL to `ngrok_url.txt`

2. Test the MCP client (in a separate terminal):
   ```bash
   # List available tools
   uv run client.py mcp_list_tools
   
   # Call the weather tool directly
   uv run client.py mcp_call_weather
   
   # Test OpenAI integration with MCP tools
   uv run client.py openai_list_tools
   uv run client.py openai_get_weather
   ```

## Project Structure

```
fastapi-to-mcp/
├── README.md          # Project documentation
├── server.py          # FastAPI app and MCP server setup
├── client.py          # MCP client examples and OpenAI integration
├── scratch.py         # Development scratch file
├── demo.zellij        # Zellij layout for development
├── pyproject.toml     # Project dependencies
├── .python-version    # Python version specification
└── ngrok_url.txt      # Generated Ngrok URL (created at runtime)
```

## Implementation Details

### FastAPI Application

The server includes a simple weather API endpoint:

```python
@app.get("/weather")
async def weather(location: str):
    # Fetches weather data from wttr.in API
    # Returns structured weather information
```

### MCP Server Conversion

FastMCP automatically converts FastAPI endpoints to MCP tools:

```python
def get_mcp_server():
    app = build_fastapi_app()
    mcp = FastMCP.from_fastapi(app=app)
    return mcp
```

### Client Examples

The project includes four client interaction patterns:

1. **Direct MCP Tool Listing**: Enumerate available tools
2. **Direct MCP Tool Calls**: Execute tools via MCP protocol
3. **OpenAI Tool Discovery**: Let OpenAI discover available tools
4. **OpenAI Tool Execution**: Have OpenAI execute tools naturally

### Ngrok Integration

The server uses a context manager for tunnel management:

```python
with ngrok_tunnel(port=8888) as ngrok_url:
    # Server runs with public access
    # URL automatically saved for client use
```

## Use Cases

- **API Modernization**: Convert legacy REST APIs to AI-accessible tools
- **Microservice Integration**: Make existing services available to AI models
- **Rapid Prototyping**: Quickly test AI tool integration without rebuilding
- **Development Testing**: Test MCP protocol implementations locally

## Development Workflow

1. **Start Server**: Run `uv run server.py` to launch FastAPI + MCP server
2. **Test Tools**: Use `uv run client.py [example]` to test different interaction patterns
3. **Iterate**: Modify FastAPI endpoints and see changes reflected automatically in MCP tools

## Examples

### Weather Tool Usage

```bash
# Direct MCP call
uv run client.py mcp_call_weather

# OpenAI natural language interaction
uv run client.py openai_get_weather
```

### Adding New Endpoints

Simply add new FastAPI routes and they become MCP tools automatically:

```python
@app.get("/calculate")
async def calculate(a: float, b: float, operation: str):
    # New endpoint becomes available as MCP tool
    pass
```

## Notes

- The Ngrok tunnel provides public access for testing with external AI services
- All FastAPI endpoints are automatically converted to MCP tools with proper schemas
- The weather API uses the free wttr.in service for demonstration
- Client examples show both direct MCP usage and OpenAI integration patterns

## Contributing

1. Fork the repository.
2. Create your feature branch.
3. Submit a pull request.

## License

MIT License - See [LICENSE](LICENSE) file for details.