# MCP Assistant Azure Prototype

A lightweight prototype that uses the Model Context Protocol (MCP) to allow an LLM to:
- Schedule Microsoft Teams meetings via Microsoft Graph API
- Read/write files to your local filesystem using the MCP Filesystem server
- Interact through a user-friendly chat interface

## Requirements

- Python 3.10+
- `.env` file with Microsoft Graph credentials
- Node.js + npx
- Gradio (`pip install gradio`)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```plaintext
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=your_api_version

# Microsoft Graph API Configuration
GRAPH_TENANT_ID=your_tenant_id
GRAPH_CLIENT_ID=your_client_id
GRAPH_CLIENT_SECRET=your_client_secret
GRAPH_USER_EMAIL=your_user_object_id
```

## Usage

### Option 1: Chat Interface (Recommended)

The chat interface provides a user-friendly way to interact with the assistant.

1. Run the Gradio chat interface:

   ```bash
   python gradio_chat.py
   ```

2. Open your browser and navigate to:

   ```
   http://127.0.0.1:7860/
   ```

3. Chat with your assistant! You can ask it to:
   - Schedule meetings
   - Check system status
   - View calendar information

### Option 2: Command Line (Original Method)

You can still use the original command line method:

1. Start the Graph Calendar MCP Server:

   ```bash
   fastmcp run graph_server.py
   ```

2. Start the Filesystem MCP Server:

   ```bash
   npx -y @modelcontextprotocol/server-filesystem ~/mcp_files
   ```

   Servers: <https://github.com/modelcontextprotocol/servers/tree/main>

3. Run the Assistant:

   ```bash
   MCP_PROMPT="Create a 30-minute meeting with [emails] today at 1pm and name the meeting Quick Sync." python main.py
   ```

   **Note**: For filesystem operations, make sure to use a file path that's within the allowed directory (`~/mcp_files`).

## How It Works

The application uses:
- Gradio for the web interface
- Asyncio for handling asynchronous operations
- Model Context Protocol (MCP) to connect the LLM with external tools
- Azure OpenAI API for the underlying AI model

## Example Prompts

Try these examples in the chat interface:

- "Schedule a meeting with [colleague@example.com] tomorrow at 2pm titled 'Project Review'"
- "What's my calendar look like for next week?"
- "Check the current system status"

## Troubleshooting

If you encounter any issues:
1. Make sure all environment variables are set correctly
2. Check that ports 7860, 8001, and 8002 are available
3. Verify that your Azure OpenAI deployment is active
4. Ensure you have the correct permissions for Microsoft Graph API