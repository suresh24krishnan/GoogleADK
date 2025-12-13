# ADK MCP Server

This project contains a fully custom **MCP (Model Context Protocol) Server** built using the **Google ADK**, along with an **ADK agent** that connects to it via stdio. The server exposes ADK tools to any MCP‑compatible client, and the agent demonstrates how to consume those tools through natural language.

---

## 📁 Project Structure

```
ADK_MCP_Server/
│
├── adk_mcp_server/               # MCP Server package
│   ├── __init__.py
│   ├── adk_mcp_server.py         # MCP server implementation (stdio)
│   └── .env                      # Environment variables (ignored)
│
├── adk_mcp_server_agent/         # ADK Agent package
│   ├── __init__.py
│   ├── agent.py                  # Agent that connects to the MCP server
│   └── .env
│
├── README.md
├── .gitignore
└── requirements.txt
```

---

## 🚀 Overview

### ✅ **ADK MCP Server**
The server exposes ADK tools over the MCP protocol using stdio.  
Currently, it exposes one tool:

- **`create_file(filename: str)`**  
  Creates an empty file in the working directory.

The server is implemented in:

```
adk_mcp_server/adk_mcp_server.py
```

It uses:

- `mcp.server.lowlevel.Server` for MCP handling  
- `FunctionTool` from ADK to wrap Python functions  
- A stdio transport layer for MCP communication  

---

### ✅ **ADK MCP Server Agent**
The agent is an ADK `LlmAgent` that:

- launches the MCP server as a subprocess  
- loads the exposed MCP tools  
- uses natural language to call those tools  
- runs on any ADK-supported LLM (e.g., Gemini, GPT‑4o)

The agent lives in:

```
adk_mcp_server_agent/agent.py
```

---

## 🛠️ Installation

Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate   # macOS/Linux
env\Scripts\activate      # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the MCP Server (Standalone)

You can run the server directly to verify it starts correctly:

```bash
python adk_mcp_server/adk_mcp_server.py
```

You should see startup logs (printed to stderr).  
The server should remain running and not exit.

---

## 🤖 Running the ADK Agent

From the project root:

```bash
adk run
```

This launches the agent defined in `agent.py`, which:

- starts the MCP server  
- loads the exposed tools  
- waits for your natural-language instructions  

---

## 💬 Example Prompts

Try these once the agent is running:

- “Create a file named `test1.txt`.”
- “Make an empty file called `notes.md`.”
- “Try creating `test1.txt` again.”
- “What tools do you have available?”
- “Help me create a placeholder file for my project.”

---

## 🧩 How It Works

1. **Agent starts**
2. **Agent launches MCP server** via `StdioServerParameters`
3. **Server initializes ADK tools**
4. **Agent requests tool list**
5. **Agent calls tools based on user intent**
6. **Server executes the ADK tool**
7. **Response flows back through MCP → ADK → LLM → user**

This creates a clean ADK → MCP → ADK loop.

---

## ✅ Future Extensions

You can easily extend this project by:

- Adding more ADK tools to the server  
- Exposing multiple tools via MCP  
- Adding stateful `ToolContext` support  
- Creating additional agents that consume the same server  
- Building a multi-agent orchestrator that uses:
  - GitHub MCP Server  
  - FileSystem MCP Server  
  - Your ADK MCP Server  

---

## 📄 License

This project is for educational and experimental use.

---
