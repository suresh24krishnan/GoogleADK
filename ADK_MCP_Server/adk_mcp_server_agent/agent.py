# agent.py

import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

# Absolute path to your ADK MCP Server script
PATH_TO_YOUR_MCP_SERVER_SCRIPT = r"C:\Users\sures\OneDrive\Personal Folders\AI Learning\Google ADK\GoogleADK\ADK_MCP_Server\adk_mcp_server\adk_mcp_server.py"

root_agent = LlmAgent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='adk_mcp_server_agent',
    instruction="Use the tools exposed by the ADK MCP Server to help the user.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='python',  # Runs your MCP server
                    args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT],
                )
            )
        )
    ],
)
