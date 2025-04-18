# MCP Assistant Azure Prototype

A lightweight prototype that uses the Model Context Protocol (MCP) to allow an LLM to:

- Schedule Microsoft Teams meetings via Microsoft Graph API
- Read/write files to your local filesystem using the MCP Filesystem server

## Requirements

- Python 3.10+
- .env file with Microsoft Graph credentials
- Node.js + npx

## Usage

### Start the Graph Calendar MCP Server:
fastmcp run graph_server.py

### Start the Filesystem MCP Server:
npx -y @modelcontextprotocol/server-filesystem ~/mcp_files

### Run the Assistant
MCP_PROMPT="Create a 30-minute meeting with nhaines888@gmail.com today at 1pm. Then write a file at ~/mcp_files/summary.txt that says: Meeting was created successfully." python main.py

Note: Make sure to use a file path that's within the allowed directory (~/mcp_files).