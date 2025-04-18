# import asyncio
# import os
# import shutil
# import subprocess
# import time
# from typing import Any

# from dotenv import load_dotenv
# from agents import Agent, Runner, trace, gen_trace_id
# from agents.mcp import MCPServerSse
# from agents.model_settings import ModelSettings
# from agents.tracing import set_tracing_disabled
# from openai import AsyncAzureOpenAI

# # Load environment variables from .env
# load_dotenv()

# # Azure OpenAI credentials
# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
# AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")

# # Disable tracing since we're using Azure OpenAI
# set_tracing_disabled(True)

# # Create Azure OpenAI client - using AsyncAzureOpenAI specifically
# openai_client = AsyncAzureOpenAI(
#     api_key=AZURE_OPENAI_API_KEY,
#     api_version=AZURE_OPENAI_API_VERSION,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT
# )

# # Set the global client
# from agents import set_default_openai_client
# set_default_openai_client(openai_client)

# # Set default API to chat completions
# from agents import set_default_openai_api
# set_default_openai_api("chat_completions")

# # Define the main function
# async def main():
#     # Start the MCP server
#     print("🚀 Starting FastMCP SSE server...")
#     process = subprocess.Popen(["uv", "run", "server.py"])
    
#     try:
#         # Give the server time to start
#         time.sleep(3)
        
#         # Generate trace ID for tracking
#         trace_id = gen_trace_id()
        
#         # Connect to the MCP server
#         async with MCPServerSse(
#             name="SSE Python Server",
#             params={"url": "http://localhost:8000/sse"}
#         ) as mcp_server:
#             with trace(workflow_name="Azure GPT + FastMCP", trace_id=trace_id):
#                 print(f"\n🔍 Trace ID: {trace_id}")
                
#                 agent = Agent(
#                     name="Assistant",
#                     instructions="You are a helpful assistant. Use the tools provided to answer questions.",
#                     mcp_servers=[mcp_server],
#                     model_settings=ModelSettings(),
#                     model=AZURE_OPENAI_DEPLOYMENT_NAME
#                 )
            
#                 # Run prompts
#                 for message in [
#                     "Add these numbers: 7 and 22.",
#                     "What's the secret word?",
#                 ]:
#                     print(f"\n\n🧠 Prompt: {message}")
                    
#                     # Use await Runner.run
#                     result = await Runner.run(
#                         starting_agent=agent,
#                         input=message
#                     )
                    
#                     print("🤖 Assistant:", result.final_output)
    
#     finally:
#         # Clean up
#         if process:
#             process.terminate()

# # Execute the main function
# if __name__ == "__main__":
#     if not shutil.which("uv"):
#         raise RuntimeError("❌ uv is not installed. Please install it: https://docs.astral.sh/uv/")
    
#     asyncio.run(main())

# import asyncio
# import os
# import shutil
# import subprocess
# import time
# from typing import Any

# from dotenv import load_dotenv
# from agents import Agent, Runner, trace, gen_trace_id
# from agents.mcp import MCPServerSse
# from agents.model_settings import ModelSettings
# from agents.tracing import set_tracing_disabled
# from openai import AsyncAzureOpenAI

# # Load environment variables from .env
# load_dotenv()

# # Azure OpenAI credentials
# AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
# AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")

# # Disable tracing since we're using Azure OpenAI
# set_tracing_disabled(True)

# # Create Azure OpenAI client - using AsyncAzureOpenAI specifically
# openai_client = AsyncAzureOpenAI(
#     api_key=AZURE_OPENAI_API_KEY,
#     api_version=AZURE_OPENAI_API_VERSION,
#     azure_endpoint=AZURE_OPENAI_ENDPOINT
# )

# # Set the global client
# from agents import set_default_openai_client
# set_default_openai_client(openai_client)

# # Set default API to chat completions
# from agents import set_default_openai_api
# set_default_openai_api("chat_completions")

# # Define the main function
# async def main():
#     # Start the MCP servers
#     print("🚀 Starting FastMCP servers...")
#     server1_process = subprocess.Popen(["uv", "run", "server.py"])
    
#     # Set the environment variable for the unique server port and host binding
#     os.environ["UNIQUE_SERVER_PORT"] = "8001"
#     os.environ["FASTMCP_HOST"] = "127.0.0.1:8001"
#     server2_process = subprocess.Popen(["uv", "run", "unique_server.py"])
    
#     try:
#         # Give the servers time to start
#         time.sleep(5)  # Extra time for both servers to start
        
#         # Generate trace ID for tracking
#         trace_id = gen_trace_id()
        
#         # Set up both MCP servers concurrently
#         sse_server1 = MCPServerSse(
#             name="Regular Tools Server",
#             params={"url": "http://localhost:8000/sse"}
#         )
        
#         sse_server2 = MCPServerSse(
#             name="Unique Information Server",
#             params={"url": "http://localhost:8001/sse"}
#         )
        
#         # Connect to both servers with proper error handling
#         async with sse_server1 as mcp_server1:
#             print("✅ Connected to server 1 (Regular Tools)")
            
#             # Try to connect to server 2, but don't fail if it's not available
#             try:
#                 async with sse_server2 as mcp_server2:
#                     print("✅ Connected to server 2 (Unique Information)")
                    
#                     # Run with both servers connected
#                     await run_with_servers(
#                         trace_id=trace_id, 
#                         mcp_servers=[mcp_server1, mcp_server2]
#                     )
#             except Exception as e:
#                 print(f"❌ Couldn't connect to server 2: {e}")
#                 print("Running with just server 1...")
                
#                 # Run with just server 1
#                 await run_with_servers(
#                     trace_id=trace_id, 
#                     mcp_servers=[mcp_server1]
#                 )
    
#     finally:
#         # Clean up
#         if 'server1_process' in locals():
#             server1_process.terminate()
#         if 'server2_process' in locals():
#             server2_process.terminate()

# async def run_with_servers(trace_id, mcp_servers):
#     """Run the agent with the provided MCP servers"""
    
#     with trace(workflow_name="Azure GPT + MCP", trace_id=trace_id):
#         print(f"\n🔍 Trace ID: {trace_id}")
        
#         # Create agent with all available MCP servers
#         agent = Agent(
#             name="Assistant",
#             instructions="""You are a helpful assistant. Use the tools provided to answer questions.
#             When asked about unique tokens or server statistics, always use the appropriate tools
#             to get this information rather than making it up.""",
#             mcp_servers=mcp_servers,
#             model_settings=ModelSettings(),
#             model=AZURE_OPENAI_DEPLOYMENT_NAME
#         )
        
#         # List of prompts to test different tools
#         prompts = [
#             "Add these numbers: 7 and 22.",
#             "What's the secret word?",
#             "Generate a unique token for me.",
#             "What are the current server statistics?"
#         ]
        
#         # Run each prompt
#         for message in prompts:
#             print(f"\n\n🧠 Prompt: {message}")
            
#             # Use await Runner.run
#             result = await Runner.run(
#                 starting_agent=agent,
#                 input=message
#             )
            
#             print("🤖 Assistant:", result.final_output)

# # Execute the main function
# if __name__ == "__main__":
#     if not shutil.which("uv"):
#         raise RuntimeError("❌ uv is not installed. Please install it: https://docs.astral.sh/uv/")
    
#     asyncio.run(main())

import asyncio
import os
import shutil
import subprocess
import time
from typing import Any

from dotenv import load_dotenv
from agents import Agent, Runner, trace, gen_trace_id
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings
from agents.tracing import set_tracing_disabled
from openai import AsyncAzureOpenAI

# Load environment variables from .env
load_dotenv()

# Azure OpenAI credentials
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")

# Disable tracing since we're using Azure OpenAI
set_tracing_disabled(True)

# Create Azure OpenAI client - using AsyncAzureOpenAI specifically
openai_client = AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# Set the global client
from agents import set_default_openai_client
set_default_openai_client(openai_client)

# Set default API to chat completions
from agents import set_default_openai_api
set_default_openai_api("chat_completions")

# Define the main function
async def main():
    print("🚀 Starting FastMCP servers...")
    server1_process = subprocess.Popen(["uv", "run", "server.py"])

    os.environ["UNIQUE_SERVER_PORT"] = "8001"
    os.environ["FASTMCP_HOST"] = "127.0.0.1:8001"
    server2_process = subprocess.Popen(["uv", "run", "unique_server.py"])

    try:
        time.sleep(5)

        trace_id = gen_trace_id()

        sse_server1 = MCPServerSse(
            name="Regular Tools Server",
            params={"url": "http://localhost:8000/sse"}
        )

        sse_server2 = MCPServerSse(
            name="Unique Information Server",
            params={"url": "http://localhost:8001/sse"}
        )

        async with sse_server1 as mcp_server1:
            print("✅ Connected to server 1 (Regular Tools)")

            try:
                async with sse_server2 as mcp_server2:
                    print("✅ Connected to server 2 (Unique Information)")

                    await run_with_servers(
                        trace_id=trace_id,
                        mcp_servers=[mcp_server1, mcp_server2]
                    )
            except Exception as e:
                print(f"❌ Couldn't connect to server 2: {e}")
                print("Running with just server 1...")

                await run_with_servers(
                    trace_id=trace_id,
                    mcp_servers=[mcp_server1]
                )

    finally:
        if 'server1_process' in locals():
            server1_process.terminate()
        if 'server2_process' in locals():
            server2_process.terminate()


async def run_with_servers(trace_id, mcp_servers):
    with trace(workflow_name="Azure GPT + MCP", trace_id=trace_id):
        print(f"\n🔍 Trace ID: {trace_id}")

        agent = Agent(
            name="Assistant",
            instructions="""You are a helpful assistant. Use the tools provided to answer questions.
            When asked about unique tokens or server statistics, always use the appropriate tools
            to get this information rather than making it up. Responses must be in a pirate tone with pirate language""",
            mcp_servers=mcp_servers,
            model_settings=ModelSettings(),
            model=AZURE_OPENAI_DEPLOYMENT_NAME
        )

        prompts = [
            "Add these numbers: 7 and 22.",
            "What's the secret word?",
            "Generate a unique token for me.",
            "What are the current server statistics?"
        ]

        for message in prompts:
            print(f"\n\n🧠 Prompt: {message}")
            result = await Runner.run(
                starting_agent=agent,
                input=message,
            )

            # Show agent reasoning from raw_output if available
            if hasattr(result, "raw_output") and isinstance(result.raw_output, dict):
                steps = result.raw_output.get("steps", [])
                if steps:
                    print("\n🔍 Agent Reasoning:")
                    for step in steps:
                        step_type = step.get("type", "UNKNOWN")
                        content = step.get("content", "").strip()
                        print(f"- [{step_type}] {content}")

            print("\n🤖 Final Output:")
            print(result.final_output)


if __name__ == "__main__":
    if not shutil.which("uv"):
        raise RuntimeError("❌ uv is not installed. Please install it: https://docs.astral.sh/uv/")

    asyncio.run(main())
