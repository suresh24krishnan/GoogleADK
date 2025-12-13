import os
import asyncio
import warnings
import logging

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv

# ---------------------------------------------------------
# Configure logging and warnings
# ---------------------------------------------------------

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)
print("Libraries imported.")

# ---------------------------------------------------------
# Load API keys from .env
# ---------------------------------------------------------

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

print("API Keys Set:")
print(f"OpenAI API Key set: {'Yes' if openai_key else 'No (MISSING!)'}")

# ---------------------------------------------------------
# Configure model (OpenAI via LiteLLM)
# ---------------------------------------------------------

AGENT_MODEL = LiteLlm(model="gpt-4o-mini")
print("\nEnvironment configured for OpenAI (LiteLLM).")

# ---------------------------------------------------------
# Tools: get_weather and get_flight_status
# ---------------------------------------------------------

def get_weather(city: str) -> dict:
    print(f"--- Tool: get_weather called for city: {city} ---")
    city_normalized = city.lower().replace(" ", "")

    mock_weather_db = {
        "newyork": {
            "status": "success",
            "report": "The weather in New York is sunny with a temperature of 25°C.",
        },
        "london": {
            "status": "success",
            "report": "It's cloudy in London with a temperature of 15°C.",
        },
        "tokyo": {
            "status": "success",
            "report": "Tokyo is experiencing light rain and a temperature of 18°C.",
        },
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have weather information for '{city}'.",
        }


def get_flight_status(flight_number: str) -> dict:
    print(f"--- Tool: get_flight_status called for flight: {flight_number} ---")

    flight_normalized = flight_number.upper().replace(" ", "")

    mock_flight_db = {
        "AI202": {
            "status": "success",
            "airline": "Air India",
            "departure": "Delhi (DEL)",
            "arrival": "Bengaluru (BLR)",
            "current_status": "Departed - On Time",
        },
        "BA118": {
            "status": "success",
            "airline": "British Airways",
            "departure": "Mumbai (BOM)",
            "arrival": "London Heathrow (LHR)",
            "current_status": "Delayed by 45 mins",
        },
        "EK501": {
            "status": "success",
            "airline": "Emirates",
            "departure": "Hyderabad (HYD)",
            "arrival": "Dubai (DXB)",
            "current_status": "Boarding",
        },
    }

    if flight_normalized in mock_flight_db:
        return mock_flight_db[flight_normalized]
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, no flight data found for '{flight_number}'.",
        }


# Quick tool tests
print(get_weather("New York"))
print(get_weather("Paris"))
print(get_flight_status("AI202"))
print(get_flight_status("QR404"))

# ---------------------------------------------------------
# Define the Agent
# ---------------------------------------------------------

weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL,
    description="Provides weather and flight status information.",
    instruction=(
        "You are a helpful weather and flight status assistant. "
        "When the user asks for the weather in a specific city, "
        "use the 'get_weather' tool. "
        "When the user asks for the flight status of a specific flight, "
        "use the 'get_flight_status' tool. "
        "If a tool returns an error, inform the user politely."
    ),
    tools=[get_weather, get_flight_status],
)

print(f"Agent '{weather_agent.name}' created using OpenAI model.")

# ---------------------------------------------------------
# Session Service and Runner
# ---------------------------------------------------------

session_service = InMemorySessionService()

APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001"


async def init_session(app_name: str, user_id: str, session_id: str):
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    print(f"Session created: App='{app_name}', User='{user_id}', Session='{session_id}'")
    return session


session = asyncio.run(init_session(APP_NAME, USER_ID, SESSION_ID))

runner = Runner(
    agent=weather_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

print(f"Runner created for agent '{runner.agent.name}'.")

# ---------------------------------------------------------
# Agent interaction helper
# ---------------------------------------------------------

async def call_agent_async(query: str, runner: Runner, user_id: str, session_id: str):
    print("\n" + "=" * 70)
    print(f">>> User Query: {query}")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        print(
            f"  [Event] Author: {event.author}, "
            f"Type: {type(event).__name__}, "
            f"Final: {event.is_final_response()}, "
            f"Content: {event.content}"
        )

        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            break

    print(f"<<< Agent Response: {final_response_text}")
    print("=" * 70)

# ---------------------------------------------------------
# Run a small conversation
# ---------------------------------------------------------

async def run_conversation():
    await call_agent_async("What is the weather like in London?", runner, USER_ID, SESSION_ID)
    await call_agent_async("How about Paris?", runner, USER_ID, SESSION_ID)
    await call_agent_async("Tell me the weather in New York", runner, USER_ID, SESSION_ID)
    await call_agent_async("Get the flight status of AI202", runner, USER_ID, SESSION_ID)


if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")
