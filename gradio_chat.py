import os
import subprocess
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import threading
import asyncio
from dotenv import load_dotenv
import gradio as gr
from agents import Agent, Runner, trace, gen_trace_id
from agents.mcp import MCPServerSse
from agents.model_settings import ModelSettings
from agents.tracing import set_tracing_disabled
from openai import AsyncAzureOpenAI

# Load environment variables
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview")

set_tracing_disabled(True)

# Initialize OpenAI client
openai_client = AsyncAzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

from agents import set_default_openai_client, set_default_openai_api
set_default_openai_client(openai_client)
set_default_openai_api("chat_completions")

# Global variables for MCP server processes and connections
graph_process = None
data_process = None
graph_mcp = None
data_mcp = None

# Function to start MCP servers
def start_mcp_servers():
    global graph_process, data_process, graph_mcp, data_mcp
    
    print("🚀 Starting MCP tool servers...")
    
    graph_process = subprocess.Popen(["python", "graph_server.py", "--port", "8001"])
    data_process = subprocess.Popen(["python", "data_server.py", "--port", "8002"])
    
    time.sleep(3)  # Let both MCP servers spin up
    
    graph_mcp = MCPServerSse(
        name="Graph Calendar Server",
        params={"url": "http://localhost:8001/sse"}
    )
    
    data_mcp = MCPServerSse(
        name="System Data Server",
        params={"url": "http://localhost:8002/sse"}
    )

# Function to stop MCP servers
def stop_mcp_servers():
    global graph_process, data_process
    
    if graph_process:
        graph_process.terminate()
        
    if data_process:
        data_process.terminate()

# Helper function to run async code in a new event loop
def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# The main chat function that interfaces with your Agent
def chat_with_agent(message, history):
    # We'll use a thread to run the async code with its own event loop
    thread = threading.Thread(
        target=lambda: setattr(threading.current_thread(), 
                              "result", 
                              run_async(async_chat_with_agent(message)))
    )
    thread.start()
    thread.join()
    return thread.result

async def async_chat_with_agent(message):
    global graph_mcp, data_mcp
    
    if graph_mcp is None or data_mcp is None:
        start_mcp_servers()
    
    trace_id = gen_trace_id()
    
    now_est = datetime.now(ZoneInfo("America/New_York"))
    today = now_est.strftime("%A, %B %d, %Y at %I:%M %p %Z")
    prompt = f"Current time is {today}. {message}"
    
    try:
        async with graph_mcp, data_mcp:
            with trace(workflow_name="Graph + Filesystem Agent", trace_id=trace_id):
                agent = Agent(
                    name="ButcherBox Assistant",
                    instructions="""You are a smart assistant for ButcherBox that can:
                    1. Schedule meetings and access calendar information
                    3. Look up company acronyms and their definitions
                    
                    When asked about acronyms, use the data_mcp tools to look them up.
                    If users ask for the meaning of acronyms, you should look them up
                    and provide the definition. You can also list all available acronyms
                    if asked.
                    
                    Always be helpful, concise, and professional in your responses.
                    """,
                    mcp_servers=[graph_mcp, data_mcp],
                    model_settings=ModelSettings(),
                    model=AZURE_OPENAI_DEPLOYMENT_NAME
                )
                
                result = await Runner.run(starting_agent=agent, input=prompt)
                return result.final_output
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create Gradio interface
def create_gradio_interface():
    try:
        # Start servers when the app loads
        start_mcp_servers()
        
        # Create the Gradio Chat Interface
        chat_interface = gr.ChatInterface(
            fn=chat_with_agent,
            type="messages",
            title="ButcherBox Assistant",
            description="I can schedule meetings and look up company acronyms",
            examples=[
                "Schedule a meeting with the team tomorrow", 
                "Show me my calendar for next week",
                "What does AOV mean?",
            ],
            cache_examples=False,  # Disable caching to avoid async issues
            chatbot=gr.Chatbot(height=500, type="messages"),  # Explicitly set type here
            textbox=gr.Textbox(
                placeholder="Ask me about meetings or company acronyms...", 
                container=False, 
                scale=7
            )
        )
        
        # Return the interface for launching
        return chat_interface
    
    except Exception as e:
        print(f"Error creating Gradio interface: {e}")
        stop_mcp_servers()
        raise e

# Main function to run the app
if __name__ == "__main__":
    try:
        # Create and launch the Gradio interface
        demo = create_gradio_interface()
        # Use a simpler launch configuration 
        demo.launch(server_name="127.0.0.1")
    finally:
        # Make sure servers get stopped when the app exits
        stop_mcp_servers()