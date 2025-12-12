import os
from google.adk.agents.llm_agent import Agent
from pydantic import BaseModel
from typing import List


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


root_agent = Agent(
   model="gemini-2.5-flash",
   name="travel_itinerary_agent",
   description="Creates structured travel itineraries for any destination",
   output_schema=TravelItinerary,
   tools=[],
)
