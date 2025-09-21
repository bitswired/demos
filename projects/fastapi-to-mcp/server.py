import os
from contextlib import contextmanager

import httpx
import ngrok
import uvicorn
from fastapi import FastAPI
from fastmcp import FastMCP
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


# 1. Define FastAPI server
def build_fastapi_app():
    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello from FastAPI!"}

    @app.get("/weather")
    async def weather(location: str):
        # Use wttr.in free weather API
        url = f"https://wttr.in/{location}?format=j1"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            weather_data = response.json()

        # Extract a simple forecast from the API response
        current_condition = weather_data.get("current_condition", [{}])[0]
        forecast = current_condition.get("weatherDesc", [{}])[0].get("value", "unknown")
        temp_C = current_condition.get("temp_C", "unknown")

        res = {
            "location": location,
            "forecast": forecast,
            "temperature_C": temp_C,
            "details": weather_data,
        }

        logger.info(f"Weather request for {location}: {res}")

        return res

    return app


# 2. Convert FastAPI app to MCP server using fastmcp
def get_mcp_server():
    app = build_fastapi_app()
    mcp = FastMCP.from_fastapi(app=app)
    return mcp


if __name__ == "__main__":
    mcp_server = get_mcp_server()
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
