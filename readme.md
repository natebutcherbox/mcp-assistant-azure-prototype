# MCP Assistant Azure Prototype

A lightweight prototype that uses the Model Context Protocol (MCP) to allow an LLM to:

- Schedule Microsoft Teams meetings via Microsoft Graph API
- Read/write files to your local filesystem using the MCP Filesystem server

## Requirements

- Python 3.10+
- .env file with Microsoft Graph credentials
- Node.js + npx

## Environment Variables
---------------------

Create a `.env` file in the root directory with the following variables:

```
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_API_VERSION=2023-12-01-preview

# Microsoft Graph API Configuration
GRAPH_TENANT_ID=your_tenant_id
GRAPH_CLIENT_ID=your_client_id
GRAPH_CLIENT_SECRET=your_client_secret
GRAPH_USER_EMAIL=your_user_object_id
```

## Usage

### Start the Graph Calendar MCP Server:
fastmcp run graph_server.py

### Start the Filesystem MCP Server:
npx -y @modelcontextprotocol/server-filesystem ~/mcp_files
<br>Servers: https://github.com/modelcontextprotocol/servers/tree/main

### Run the Assistant
MCP_PROMPT="Create a 30-minute meeting with [emails] today at 1pm and name the meeting Quick Sync.
<br>Then write a file called summary.txt that says: Meeting was created successfully."  python main.py

Note: Make sure to use a file path that's within the allowed directory (~/mcp_files).