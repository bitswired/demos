import uvicorn
from fastmcp import FastMCP
from fastmcp.client.transports import StdioTransport
from fastmcp.server.proxy import ProxyClient


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


# Run the proxy (e.g., via stdio for Claude Desktop)
if __name__ == "__main__":
    mcp_server = build_mcp_proxy()
    app = mcp_server.http_app(stateless_http=True)

    port = 8888

    # Run with HTTPS using uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=port,
    )
