
# Gemini Agent — Google ADK + Google Search Tool

This project showcases a minimal agent built with **Google ADK** that uses the **`gemini-2.5-flash`** model and the built-in **Google Search Tool** to answer user questions with fresh web results.

---

## 📁 Project Structure

```
BUILTINTOOLS_GOOGLESEARCH/
├── builtintools_agent/
│   ├── agent.py              # defines the Gemini agent and search tool
│   ├── __init__.py           # enables package import
│   ├── .env                  # contains GOOGLE_API_KEY (ignored by Git)
│   ├── .adk/                 # ADK runtime state (ignored)
│   └── __pycache__/          # Python cache (ignored)
├── requirements.txt          # dependencies
├── .gitignore                # ignore rules
└── README.md                 # project documentation
```

---

## 🔍 Agent Overview

**Agent Name:** `gemini_agent`  
**Model:** `gemini-2.5-flash`  
**Tool:** `google_search` (built-in ADK tool)

### Agent Instruction

> "I can answer your questions by searching the internet. Just ask me anything!"

---

## 🛠️ Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your Gemini API key

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your-real-key-here
```

This key must be valid and tied to a Google Cloud project with access to Gemini.

---

## 🚀 Running the Agent

### Option 1 — ADK CLI

```bash
adk run builtintools_agent
```

### Option 2 — Python script

```python
from builtintools_agent.agent import root_agent

response = root_agent.run("What are the latest AI trends?")
print(response)
```

---

## ⚠️ Quota Notes

- `gemini-2.5-flash` is a **paid model** and may trigger quota errors if your free tier is exhausted.
- To avoid `RESOURCE_EXHAUSTED` errors, ensure your Google Cloud project has billing enabled or switch to a free-tier model like `gemini-1.5-flash`.

---

## ✅ Git Hygiene

This repo includes a `.gitignore` that excludes:

- `.env` files  
- `.adk/` runtime folders  
- `__pycache__/`  
- `env/` virtual environment  

to keep commits clean and secure.

---

## 📌 Summary

This project demonstrates:

- ✅ How to build a minimal ADK agent  
- ✅ How to use the built-in Google Search Tool  
- ✅ How to integrate Gemini models with ADK tools

Perfect for showcasing Google ADK’s tool-calling capabilities in a clean, reproducible way.
```

---
