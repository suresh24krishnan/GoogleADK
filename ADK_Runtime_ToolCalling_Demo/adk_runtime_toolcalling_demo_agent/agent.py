from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# ---------------------------------------------------------
# Minimal placeholder agent for ADK auto-discovery
# ---------------------------------------------------------
# IMPORTANT:
# The real runtime demo (with Runner, SessionService, tools, etc.)
# is implemented in weather_runtime_demo.py at the project root.
# ---------------------------------------------------------

agent = Agent(
    name="runtime_toolcalling_placeholder",
    model=LiteLlm(model="gpt-4o-mini"),
    description="Placeholder agent for ADK auto-discovery.",
    instruction=(
        "This is a placeholder agent. "
        "The full runtime demonstration, including tool calling, "
        "session management, and event streaming, is implemented "
        "in weather_runtime_demo.py."
    ),
)
