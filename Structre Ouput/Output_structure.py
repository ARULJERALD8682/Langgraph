from pydantic import BaseModel,Field
from langgraph.graph.message import MessagesState

class FinalResponse(BaseModel):
    """Responed to user like this"""
    Departure_AirportName: str = Field(description="It descripes departure airport name")
    Arrival_AirportName : str = Field(description="it descripes arrival airport name")
    price : int = Field(description="it descripes the price")

class AgentState(MessagesState):

    final_response : FinalResponse

