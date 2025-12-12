
# GitHub Agent with MCP Integration

This agent is designed to help users interact with GitHub repositories using natural language. It leverages the [Google ADK](https://github.com/google/adk) framework and MCP toolsets to provide read-only access to GitHub data via the Copilot MCP API.

## 🧠 Purpose

The `github_agent` enables users to:

- Explore repository structure and contents
- Search for files, functions, and code snippets
- Retrieve metadata like issues, pull requests, commits, and contributors
- Compare branches, view diffs, and inspect release history
- Ask natural language questions about GitHub projects

## ⚙️ Setup

1. Clone this repository.
2. Create a `.env` file in the `github_agent` folder with your GitHub token:

   ```env
   GITHUB_TOKEN=your_github_token_here
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the agent using your preferred ADK launcher or integration.

## 🧩 Agent Configuration

```python
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

root_agent = Agent(
  model='gemini-2.5-flash',
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
```

## 💬 Example Questions You Can Ask This Agent

- “Show me the folder structure of `suresh24krishnan/GoogleADK`.”
- “List all Python files in `suresh24krishnan/GoogleADK/DifferentModels_Agent`.”
- “Show me the README for `suresh24krishnan/GoogleADK/FunctionTools`.”
- “Search for all functions named `run` in `suresh24krishnan/GoogleADK`.”
- “List all open issues in `suresh24krishnan/GoogleADK`.”
- “Show me the latest commits in `suresh24krishnan/GoogleADK`.”
- “Compare branch `main` with `dev` in `suresh24krishnan/GoogleADK`.”
- “Who are the top contributors to `suresh24krishnan/GoogleADK`?”

## 📦 Folder Structure

```
github_agent/
├── agent.py
├── __init__.py
├── .env              # Local credentials (ignored)
├── .adk/             # ADK session files (ignored)
├── __pycache__/      # Runtime cache (ignored)
.gitignore
README.md
requirements.txt
```

## 🚫 Notes

- This agent is **read-only** and cannot modify GitHub data.
- Session files and environment variables are excluded via `.gitignore`.

---
