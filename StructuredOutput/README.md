
# StructuredOutput Agents

This module contains a collection of Google ADK agents designed to produce **structured, validated outputs** using **Pydantic schemas**. Each agent is isolated in its own folder, maintains its own environment configuration, and exposes a clean `Agent` instance ready for orchestration or direct invocation.

Structured output ensures that every response conforms to a predictable schema — ideal for downstream automation, UI rendering, or multi‑agent workflows.

---

## 📁 Project Structure

```
StructuredOutput/
│
├── mail_agent/
│   ├── agent.py
│   ├── schemas.py
│   ├── __init__.py
│   ├── .env
│   └── .adk/          # runtime state (ignored)
│
├── travel_itinerary_agent/
│   ├── agent.py
│   ├── schemas.py
│   ├── __init__.py
│   ├── .env
│   └── .adk/          # runtime state (ignored)
│
├── requirements.txt
├── .gitignore
└── README.md
```

Each agent folder contains:

- **`agent.py`** — ADK agent definition using the schema  
- **`.env`** — local environment variables (API keys, config)  
- **`.adk/`** — ADK runtime session files (ignored by Git)

---

## ✉️ Mail Agent

**Folder:** `mail_agent/`  
**Purpose:** Generates structured email content with a subject and body.

### Output Schema

```python
class MailOutput(BaseModel):
    subject: str
    body: str
```

### Example Use Cases

- Drafting professional emails  
- Auto‑generating templated responses  
- Integrating into workflow automation  

---

## 🌍 Travel Itinerary Agent

**Folder:** `travel_itinerary_agent/`  
**Purpose:** Produces multi‑day travel itineraries with structured day plans.

### Output Schema

```python
class DayPlan(BaseModel):
    day: int
    title: str
    activities: List[str]
    notes: str = ""

class TravelItinerary(BaseModel):
    destination: str
    total_days: int
    best_time_to_visit: str
    itinerary: List[DayPlan]
```

### Example Use Cases

- Travel planning apps  
- Personalized itinerary generation  
- Integrating into trip‑recommendation systems  

---

## 🔧 Installation

From the `StructuredOutput/` directory:

```bash
pip install -r requirements.txt
```

Each agent requires a `.env` file containing your Gemini API key:

```
GOOGLE_API_KEY=your-key-here
```

---

## 🚀 Using an Agent

### Mail Agent

```python
from mail_agent.agent import mail_agent

response = mail_agent.run("Write a welcome email for new employees.")
print(response)
```

### Travel Itinerary Agent

```python
from travel_itinerary_agent.agent import travel_itinerary_agent

response = travel_itinerary_agent.run("Plan a 5-day trip to Tokyo.")
print(response)
```

---

## 🧹 Git Hygiene

This module includes a `.gitignore` that ensures:

- `.env` files  
- `.adk/` runtime folders  
- `__pycache__/`  

are never committed.

---

## ➕ Extending the Module

To add a new structured-output agent:

1. Create a new folder under `StructuredOutput/`
2. Add:
   - `schemas.py`
   - `agent.py`
   - `.env`
   - `.adk/` (auto-created)
3. Register or import the agent wherever needed

This structure scales cleanly for dozens of agents.

---

## ✅ Summary

The `StructuredOutput` module provides:

- Clean, modular agent design  
- Strongly typed Pydantic schemas  
- Easy extensibility  
- ADK‑ready agent definitions  
- Safe Git hygiene with isolated `.env` and `.adk` files  

Perfect for building a growing library of structured-output agents.
```

