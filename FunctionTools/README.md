

```
FUNCTIONTOOLS/
├── env/                          # virtual environment
├── filetool_agent/
│   ├── agent.py                  # contains root_agent with create_file,folder,delete file,folder,list tool
│   ├── .env                      # local API key (should be ignored)
│   ├── .adk/                     # runtime state (should be ignored)
│   ├── __pycache__/             # Python cache (should be ignored)
│   └── __init__.py              # enables package import
├── requirements.txt             # dependencies
├── .gitignore                   # ignore rules
└── README.md                    # project documentation
```

---

## ✅ `.gitignore` (place in FUNCTIONTOOLS root)

```gitignore
# Secrets
.env
*/.env

# ADK runtime
.adk/
*/.adk/

# Python cache
__pycache__/
*/__pycache__/
```

This ensures `.env`, `.adk`, and `__pycache__` are never committed.

---

## ✅ `requirements.txt` (minimal and sufficient)

```txt
google-adk
google-genai
python-dotenv
```

Add `litellm` only if you use it.

---

## ✅ `README.md` (suggested content)

```markdown
# FunctionTools Agent

This project defines a Google ADK agent with tool-augmented capabilities for file creation.

## 📁 Structure

- `filetool_agent/agent.py` — defines `root_agent` with `create_file` tool
- `filetool_agent/.env` — contains `GOOGLE_API_KEY` (ignored by Git)
- `requirements.txt` — dependencies
- `.gitignore` — excludes secrets and runtime files

## 🛠️ Tool: `create_file(filename: str)`

Creates an empty file in the current directory. Returns a success or error message.

## 🚀 Running the Agent

Ensure `.env` contains:

```
GOOGLE_API_KEY=your-key-here
```

Then run:

```bash
adk run filetool_agent
```

## ✅ Git Hygiene

This repo ignores:

- `.env` files  
- `.adk/` runtime folders  
- `__pycache__/`  

to keep commits clean and secure.
```

---