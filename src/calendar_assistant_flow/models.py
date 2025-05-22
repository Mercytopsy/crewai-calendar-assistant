from typing import Tuple, List, Optional, Union
from pydantic import BaseModel, Field,EmailStr
from datetime import date, datetime, time


class AgentSelection(BaseModel):
    chosen_assistant: List[str] = []

class MeetingCrafter(BaseModel):
    """Model for crafting meetings and events"""
    summary: str = Field(..., description="Meeting Title")
    location: Optional[str] = Field(None, description="The location of the event")
    description: Optional[str] = Field(None, description="A short description of the event is all about")
    start: str = Field(..., description="The Start datetime the user sent in string format")
    end: str  = Field(..., description="end datetime the user sent in string format")
    attendees: List[EmailStr] = Field(None, description="The guest joining the meeting")

class MeetingScheduler(BaseModel):
    """Model for meeting scheduler"""
    summary: str = Field(..., description="The meeting title scheduled")
    description: Optional[str] = Field(..., description="A short summary of the response")


class DateInterpreter(BaseModel):
    """Model for date interpretation"""
    start: Optional[str] = Field(..., description="The start date and time computed")
    end: Optional[str] = Field(..., description="The end date and time computed")
    
  
class AvailabilityChecker(BaseModel):
    """Model for availability checker"""
    date: Optional[datetime] = Field(..., description="users available date from the calendar")
    available: List[Tuple[time, time]] = Field(..., description= "List of available time intervals")
    # start: Optional[str] = Field(..., description="The start date and time computed")
