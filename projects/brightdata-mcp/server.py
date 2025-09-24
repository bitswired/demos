import os
from contextlib import contextmanager

import ngrok
import uvicorn
from fastmcp import FastMCP
from fastmcp.client.transports import StdioTransport
from fastmcp.server.proxy import ProxyClient
from loguru import logger


def get_server_url():
    with open("ngrok_url.txt", "r") as f:
        return f.read().strip() + "/mcp"


@contextmanager
def ngrok_tunnel(port: int):
    """Context manager for ngrok tunnel"""
    logger.info(f"🔗 Setting up Ngrok tunnel for port {port}...")

    # Setup ngrok
    tunnel = ngrok.forward(port, authtoken=os.getenv("NGROK_AUTHTOKEN"))

    ngrok_url = tunnel.url()
    logger.info(f"✅ Ngrok tunnel active: {ngrok_url}")
    logger.info(f"🌐 MCP endpoint: {ngrok_url}/mcp")
    logger.info("-" * 50)

    with open("ngrok_url.txt", "w") as f:
        f.write(ngrok_url)

    try:
        yield ngrok_url
    finally:
        logger.info("\n🔌 Disconnecting Ngrok tunnel...")
        ngrok.disconnect()
        logger.info("👋 Tunnel disconnected!")


def build_mcp_proxy():
    brightdata_api_key = os.getenv("BRIGHTDATA_API_KEY")
    if not brightdata_api_key:
        raise ValueError("BRIGHTDATA_API_KEY environment variable is not set")

    transport = StdioTransport(
        command="npx",
        args=["@brightdata/mcp"],
        env={
            "API_TOKEN": brightdata_api_key,
            "PRO_MODE": "true",
        },
    )

    # Create a proxy with full MCP feature support
    proxy = FastMCP.as_proxy(
        ProxyClient(transport=transport), name="BrightData MCP Proxy"
    )

    return proxy


# Run the proxy (e.g., via stdio for Claude Desktop)
if __name__ == "__main__":
    mcp_server = build_mcp_proxy()
    app = mcp_server.http_app(stateless_http=True)

    port = 8888

    # Use ngrok context manager
    with ngrok_tunnel(port=port) as ngrok_url:
        logger.info("🚀 Starting MCP server...")
        logger.info("📋 Local endpoint: https://localhost:8888/mcp")
        logger.info("Press Ctrl+C to stop the server")

        # Run with HTTPS using uvicorn
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=port,
        )
