
# GitHub MCP Server (Stdio) Agent

This project provides a GitHub-integrated agent built using the Google ADK framework and the Model Context Protocol (MCP).  
It connects to GitHub through the **local Stdio-based MCP server** provided by the npm package `@modelcontextprotocol/server-github`.

---

## ✅ Purpose

This agent allows natural-language interaction with GitHub repositories, including:

- Listing files in a repo  
- Reading file contents  
- Searching code  
- Fetching repo metadata  
- Inspecting branches, issues, and pull requests  

All operations are performed through the MCP GitHub server running locally via `npx`.

---

## ✅ Architecture Overview

- **Agent Framework:** Google ADK (`google.adk.agents.llm_agent.Agent`)
- **Model:** `gemini-2.5-flash`
- **Transport:** Stdio (local process)
- **MCP Server:** `@modelcontextprotocol/server-github`
- **Authentication:** GitHub Personal Access Token (Fine-Grained)

---

## ✅ Code Summary

```python
root_agent = Agent(
    model="gemini-2.5-flash",
    name="github_agent",
    instruction="Help users interact with GitHub repositories using MCP.",
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=r"C:\Program Files\nodejs\npx.cmd",
                    args=["-y", "@modelcontextprotocol/server-github"],
                    env={"GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN}
                )
            )
        )
    ]
)
```

---

## ✅ Requirements

- Python 3.10+
- Node.js + npm
- Google ADK installed
- GitHub Personal Access Token with appropriate scopes
- The npm MCP server:

```bash
npm install -g @modelcontextprotocol/server-github
```

---

## ✅ Environment Setup

Create a `.env` file:

```
GITHUB_TOKEN=ghp_your_token_here
```

Activate your virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

---

## ✅ Running the Agent

Run your Python script:

```bash
python agent.py
```

The agent will automatically launch:

```
npx.cmd -y @modelcontextprotocol/server-github
```

and establish an MCP session.

---

## ✅ Example Queries

Try these once the agent is running:

- “List all files in the repo `GoogleADK` owned by `suresh24krishnan` on the `main` branch.”
- “Read the README.md file from the repo.”
- “Search for Python files in the repo.”
- “Show me the metadata for the repository.”

---

## ✅ Project Structure

```
GitHub_MCP_Server_Stdio/
│
├── github_mcp_agent/
│   ├── agent.py
│   ├── __init__.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ✅ Notes

- This agent uses the **local** MCP GitHub server, not the hosted Copilot MCP endpoint.
- Stdio transport requires using the `.cmd` version of `npx` on Windows.
- The agent is read-only unless your token includes write scopes.

---

## ✅ License

This project is part of the Google ADK ecosystem.  
Refer to the ADK license for usage terms.

```
