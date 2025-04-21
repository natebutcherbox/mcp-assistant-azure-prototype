import asyncio
import os
import subprocess
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from agents import Agent, Runner, trace, gen_trace_id
from agents.mcp import MCPServerSse, MCPServerStdio
from agents.model_settings import ModelSettings
from agents.tracing import set_tracing_disabled
from openai import AsyncAzureOpenAI

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")

set_tracing_disabled(True)

openai_client = AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

from agents import set_default_openai_client, set_default_openai_api
set_default_openai_client(openai_client)
set_default_openai_api("chat_completions")


async def main():
    print("🚀 Starting MCP tool servers...")

    graph_process = subprocess.Popen(["python", "graph_server.py", "--port", "8001"])
    data_process = subprocess.Popen(["python", "data_server.py", "--port", "8002"])

    try:
        time.sleep(3)  # Let both MCP servers spin up

        trace_id = gen_trace_id()

        graph_mcp = MCPServerSse(
            name="Graph Calendar Server",
            params={"url": "http://localhost:8001/sse"}
        )

        data_mcp = MCPServerSse(
            name="System Data Server",
            params={"url": "http://localhost:8002/sse"}
        )


        async with graph_mcp, data_mcp:
            with trace(workflow_name="Graph + Filesystem Agent", trace_id=trace_id):
                user_prompt = os.environ.get("MCP_PROMPT", "Schedule a meeting")

                now_est = datetime.now(ZoneInfo("America/New_York"))
                today = now_est.strftime("%A, %B %d, %Y at %I:%M %p %Z")
                prompt = f"Current time is {today}. {user_prompt}"

                print(f"\n🧠 Prompt: {prompt}\n")

                agent = Agent(
                    name="Graph + Data Assistant",
                    instructions="You are a smart assistant that can schedule meetings and provide system information.",
                    mcp_servers=[graph_mcp, data_mcp],
                    model_settings=ModelSettings(),
                    model=AZURE_OPENAI_DEPLOYMENT_NAME
                )

                result = await Runner.run(starting_agent=agent, input=prompt)

                print("\n🤖 Final Output:\n")
                print(result.final_output)

    finally:
        if graph_process:
            graph_process.terminate()
        if data_process:
            data_process.terminate()


if __name__ == "__main__":
    asyncio.run(main())
