import asyncio
from fastmcp import FastMCP
import datetime
import os
import uuid

mcp = FastMCP("Unique Information Server")

@mcp.tool()
def get_unique_token() -> str:
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())
    env_specific = os.environ.get("MCP_SECRET", "default_secret_42")
    unique_token = f"TOKEN-{current_time}-{unique_id[:8]}-{env_specific}"
    print(f"[debug] Generated unique token: {unique_token}")
    return unique_token

@mcp.tool()
def get_current_server_stats() -> dict:
    import random
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    memory_usage = random.randint(200, 500)
    cpu_usage = random.uniform(5.0, 25.0)
    server_uptime = random.randint(1000, 9999)
    stats = {
        "timestamp": current_time,
        "memory_mb": memory_usage,
        "cpu_percent": round(cpu_usage, 2),
        "uptime_seconds": server_uptime,
        "server_id": "mcp-unique-" + str(random.randint(10000, 99999))
    }
    print(f"[debug] Server stats generated: {stats}")
    return stats

if __name__ == "__main__":
    asyncio.run(
        mcp.run_sse_async(
            host="127.0.0.1",
            port=8001,
            log_level="debug"
        )
    )
