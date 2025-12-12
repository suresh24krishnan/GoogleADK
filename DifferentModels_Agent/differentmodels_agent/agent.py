# from google.adk.agents.llm_agent import Agent
# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )


import os
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
root_agent = Agent(
   model=LiteLlm(model="openai/gpt-4o"),
   name="gpt_agent",
   description="You are a helpful assistant to answer user queries",
   tools=[],
)