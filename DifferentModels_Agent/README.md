# UseDifferentModels

This project demonstrates how to build agents that can switch between **Google Gemini** and **OpenAI GPT‑4o** models using environment variables. It’s part of the consolidated **GoogleADK** repository.

---

## 🚀 Features
- Modular `Agent` class with provider detection (`google` or `openai`).
- Supports both CLI (`adk run`) and Web UI (`adk web --port 8080`).
- Environment‑based configuration with `.env` files.
- Clean separation of Gemini and OpenAI SDKs.

---

## 📂 Project Structure

UseDifferentModels/ 

├── agent.py # Main agent logic 
├── init.py # Package initializer 
├── .env # Environment variables (API keys, provider, model) 
├── requirements.txt # Dependencies 
└── .adk/ # ADK metadata


---

## ⚙️ Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/GoogleADK.git
   cd GoogleADK/UseDifferentModels

Create a virtual environment

python -m venv env
source env/bin/activate   # macOS/Linux
env\Scripts\activate      # Windows

Install dependencies

pip install -r requirements.txt

Configure .env
Add your API keys and provider settings:
# For OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-your-openai-key

# Or for Gemini
LLM_PROVIDER=google
LLM_MODEL=gemini-1.5-flash
GOOGLE_API_KEY=your-google-key

Running the Agent
adk run openai_agent

Web UI
adk web --port 8080
Then open http://localhost:8080 in your browser.

📌 Notes
agent.py exposes root_agent so ADK can discover it.

.gitignore excludes local env/ folders, caches, and secrets.

Switch providers by editing .env.

Each project in the GoogleADK repo has its own README.md for clarity.

🛠️ Dependencies
OpenAI Python SDK

LiteLLM

Google Generative AI SDK

python-dotenv

📖 License
This project is part of the GoogleADK repository. Use and modify freely for learning and experimentation.


