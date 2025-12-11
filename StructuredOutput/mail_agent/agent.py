import os
from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel


class MailOutput(BaseModel):
   subject: str
   body: str


root_agent = Agent(
  model='gemini-2.5-flash',
  name='mail_agent',
  description='A helpful assistant for writing mails',
  output_schema=MailOutput,
  tools=[]
)

