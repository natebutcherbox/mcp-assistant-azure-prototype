# server.py
from fastmcp import FastMCP

mcp = FastMCP("Assistant Tool Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print(f"[debug] add({a}, {b})")
    return a + b

@mcp.tool()
def get_secret_word() -> str:
    """Returns a random secret word."""
    import random
    return random.choice(["pineapple", "velocity", "sapphire"])

if __name__ == "__main__":
    mcp.run(transport="sse")