import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import google_search
from dotenv import load_dotenv

load_dotenv()

root_agent = Agent(
   model="gemini-2.5-flash",
   name="gemini_agent",
   description="Agent to answer questions using Google Search.",
   instruction="I can answer your questions by searching the internet. Just ask me anything!",
   tools=[google_search],
)


