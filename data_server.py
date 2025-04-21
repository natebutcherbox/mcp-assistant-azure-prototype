import json
import logging
from fastmcp import FastMCP

# Set up logging with more granularity
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger("data_server")
# Ensure FastMCP internal logs are captured
fastmcp_logger = logging.getLogger("mcp.server")
fastmcp_logger.setLevel(logging.DEBUG)

# Create the FastMCP server
data_mcp = FastMCP("System Data Server")

# Define a resource using the @resource decorator
@data_mcp.resource(
    uri="data://system-status",
    name="SystemStatus",
    description="Returns the current system status information",
    mime_type="application/json"
)
def get_system_status() -> dict:
    """Returns current system status and uptime info."""
    logger.info("get_system_status resource function called!")
    return {
        "status": "operational",
        "uptime_hours": 234,
        "last_checked": "2025-04-18T14:00:00Z"
    }

# Add a simple tool as well, in case resources aren't properly supported
@data_mcp.tool()
def check_system_status() -> dict:
    """Returns the current system operational status and uptime."""
    logger.info("check_system_status tool function called!")
    return {
        "status": "operational",
        "uptime_hours": 234,
        "last_checked": "2025-04-18T14:00:00Z"
    }

# Log what's been registered
logger.info("Registered MCP Resources:")
for uri in data_mcp._resource_manager.get_resources():
    logger.info(f" - {uri}")

logger.info("Registered MCP Tools:")
for tool in data_mcp._tool_manager.get_tools():
    logger.info(f" - {tool}")

if __name__ == "__main__":
    import asyncio
    logger.info("Starting System Data Server on http://127.0.0.1:8002")
    asyncio.run(
        data_mcp.run_sse_async(
            host="127.0.0.1",
            port=8002,
            log_level="debug"
        )
    )