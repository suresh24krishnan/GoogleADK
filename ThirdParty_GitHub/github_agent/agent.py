import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams


from dotenv import load_dotenv
load_dotenv()


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
root_agent = Agent(
  model=LiteLlm(model="openai/gpt-4o"),
  name="github_agent",
  instruction="Help users get information from GitHub",
  tools=[
      McpToolset(
          connection_params=StreamableHTTPServerParams(
              url="https://api.githubcopilot.com/mcp/",
              headers={
                  "Authorization": f"Bearer {GITHUB_TOKEN}",
                  "X-MCP-Toolsets": "all",
                  "X-MCP-Readonly": "true"
              },
          ),
      )
  ],
)
