
# FileSystem MCP Server Agent

This agent enables file system management through the Model Context Protocol (MCP), allowing LLMs to interact with local files using structured tools. It is built using the Google ADK framework and integrates with the `@modelcontextprotocol/server-filesystem` backend via `npx`.

## 🧠 Purpose

The `filesystem_assistant_agent` is designed to help users:

- List files and directories
- Read file contents
- Perform basic file operations
- Interface with a local MCP server using standard I/O

## 🏗️ Architecture

- **Agent Framework**: [`google.adk.agents.llm_agent.Agent`](https://github.com/google/adk)
- **Model**: `LiteLlm(model="openai/gpt-4o")`
- **Toolset**: `McpToolset` with `StdioConnectionParams`
- **Backend**: `@modelcontextprotocol/server-filesystem` via `npx`

## 📁 Target Folder

The agent operates on the following folder path:

```
C:\Users\sures\OneDrive\Personal Folders\AI Learning\Google ADK\GoogleADK
```

This path is passed to the MCP server as the root directory for file operations.

## 🚀 How It Works

```python
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
                timeout=60,
            ),
        )
    ],
)
```

## 🛠️ Setup

1. Ensure `npx` is installed (via Node.js).
2. Install the MCP server package:

```bash
npx -y @modelcontextprotocol/server-filesystem <target-folder>
```

3. Run the agent script to initialize the assistant.

## 📦 Files

- `agent.py` — main agent definition
- `__init__.py` — module initializer
- `requirements.txt` — dependencies
- `.gitignore` — excludes runtime artifacts
- `README.md` — this file

## 🧪 Notes

- Timeout is increased to 60s to accommodate slower file operations.
- You can customize the `TARGET_FOLDER_PATH` to point to any directory.
- The agent is modular and can be extended with additional MCP tools.

## 📄 License

This project is part of the Google ADK ecosystem. Refer to the ADK license for usage terms.

```
