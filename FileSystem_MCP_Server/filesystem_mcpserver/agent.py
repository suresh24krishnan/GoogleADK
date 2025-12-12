import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StdioServerParameters
from mcp import StdioServerParameters as MCPStdioServerParameters  # if needed, but you already imported

TARGET_FOLDER_PATH = r"C:\Users\sures\OneDrive\Personal Folders\AI Learning\Google ADK\GoogleADK"

print("MCP PATH:", os.path.abspath(TARGET_FOLDER_PATH))

root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name="filesystem_assistant_agent",
    instruction="Help the user manage their files. You can list files, read files, etc.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-filesystem",
                        os.path.abspath(TARGET_FOLDER_PATH),
                    ],
                ),
                timeout=60,   # 🔥 increase from default 5s to 60s
            ),
        )
    ],
)
