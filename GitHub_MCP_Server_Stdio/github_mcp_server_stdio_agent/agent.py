
import os
from dotenv import load_dotenv

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables.")

root_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name="github_agent",
    instruction="Help users interact with GitHub repositories using MCP.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=r"C:\Program Files\nodejs\npx.cmd",   # ✅ FIXED
                    args=[
                        "-y",
                        "@modelcontextprotocol/server-github",
                    ],
                    env={
                        "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
                    }
                )
            )
        )
    ]
)
