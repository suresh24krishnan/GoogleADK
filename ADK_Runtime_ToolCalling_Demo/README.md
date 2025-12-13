
# ADK Runtime ToolCalling Demo

This project demonstrates how to use the **Google ADK runtime manually** with:

- ✅ OpenAI (via LiteLLM)
- ✅ Custom tools (weather + flight status)
- ✅ Manual session management
- ✅ Event streaming
- ✅ Multi-turn conversations
- ✅ ADK Runner API

Unlike typical ADK projects, this one **does not rely on auto-discovered agents**.  
Instead, it shows how ADK works *under the hood* using a fully manual runtime pipeline.

---

## 📁 Project Structure

```
ADK_Runtime_ToolCalling_Demo/
│
├── weather_runtime_demo.py        # Full manual ADK runtime demo (OpenAI + tools)
├── requirements.txt
├── README.md
│
└── adk_runtime_toolcalling_demo_agent/
    ├── agent.py                   # Minimal placeholder agent for ADK auto-discovery
    └── __init__.py
```

### ✅ Why a placeholder agent?
ADK requires an agent folder for `adk run` and `adk web` to load.  
However, the real logic lives in `weather_runtime_demo.py`, not in the agent folder.

This keeps ADK happy while allowing you to explore the **manual runtime**.

---

## 🚀 Features Demonstrated

### ✅ 1. Manual ADK Runtime
This project uses:

- `Runner`
- `InMemorySessionService`
- `run_async()`
- Event streaming
- Multi-turn session handling

This is the **lowest-level ADK API**, giving full control over the agent lifecycle.

---

### ✅ 2. Tool Calling
Two mock tools are implemented:

- `get_weather(city)`
- `get_flight_status(flight_number)`

The LLM automatically:

1. Detects user intent  
2. Chooses the correct tool  
3. Generates a structured tool call  
4. Receives the tool result  
5. Produces a final natural-language response  

This is the core of ADK’s tool-calling engine.

---

### ✅ 3. OpenAI Model Integration (via LiteLLM)

The project uses:

```
LiteLlm(model="gpt-4o-mini")
```

This avoids Gemini quota issues and keeps the runtime fast and reliable.

---

### ✅ 4. Multi-turn Conversations

Sessions persist across multiple queries using:

```
InMemorySessionService()
```

This allows the agent to maintain context across turns.

---

## 🛠️ Setup Instructions

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Add your OpenAI API key to `.env`

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_key_here
```

### 3. Run the runtime demo

```
python weather_runtime_demo.py
```

You will see:

- Tool calls  
- Event streaming  
- Final responses  
- Multi-turn behavior  

---

## 🌐 Why `adk web` Does Not Work Here

This project uses a **manual ADK runtime**, not an auto-discovered agent.

`adk web` only works with:

- simple agent definitions  
- no manual Runner  
- no asyncio.run  
- no custom session logic  

Since this project intentionally bypasses the ADK web runtime,  
`adk web` will load only the placeholder agent — not the runtime demo.

This is expected.

---

## 🔮 Possible Extensions

You can extend this project into:

### ✅ Real Weather API Integration
- OpenWeatherMap  
- WeatherAPI  

### ✅ Real Flight Status Integration
- AviationStack  
- FlightAware  

### ✅ Agent State
Let the agent remember:
- last city  
- last flight  
- preferences  

### ✅ Router Agent
Automatically route queries to:
- Weather agent  
- Flight agent  
- Other agents  

### ✅ Agent Teams
Combine multiple agents into a coordinated system.

### ✅ RAG + Tools
Add retrieval-augmented generation with tool calling.

---

## 📜 License

MIT License

---

If you build on this project, feel free to add your own sections or badges.  
Happy experimenting with ADK internals and multi-agent architectures!
```

---
