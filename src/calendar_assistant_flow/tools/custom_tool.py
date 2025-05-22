from crewai.tools import BaseTool
from typing import Type, List, Optional, Union
from pydantic import BaseModel, Field, EmailStr

from datetime import date, datetime, time


from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from crewai.tools import BaseTool
from typing import Type, List, Optional, Literal, Union
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, timezone, time
from tzlocal import get_localzone
import pickle
import os





class MeetingDetails(BaseModel):
    """Model for Meeting details."""
    summary: str = Field(..., description="Meeting Title")
    location: Optional[str] = Field(None, description="The location of the event")
    description: Optional[str] = Field(None, description="A short description of the event is all about")
    start: str = Field(..., description="The time the event will start")
    end: str = Field(..., description="The time the event will end")
    attendees: List[EmailStr] = Field(None, description="The guest joining the meeting")
    # reminders: Optional[dict] = Field(None, description="The default reminder time")


class MeetingScedulerTool(BaseTool):
    """Tool to create meeting using the google calendar API."""
    name: str = "create meetings"
    description: str = "used for creating meetings and events on google calendar"
    args_schema: Type[BaseModel] = MeetingDetails


    def connect_to_api(self):
        """Shows basic usage of the Google Calendar API.
        """
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build("calendar", "v3", credentials=creds)
        return service


  
    def parse_dates(self, start_dt, end_dt):
            
        time_zone = str(get_localzone())

        start_time = datetime.fromisoformat(start_dt) # Convert string to datetime
        end_time = datetime.fromisoformat(end_dt)

        start={"dateTime": start_time.isoformat(), "timeZone": time_zone}
        end={"dateTime": end_time.isoformat(), "timeZone": time_zone}

        reminders = {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ]
            }
      
        return start, end, reminders
    

    def create_event(self, input, service):

        service.events().insert(calendarId='primary', body=input, sendUpdates='all').execute()

        print('Event created successfully')





    def _run(self, summary: str, location: Optional[str], description: Optional[str], 
             start: str, end: str, attendees: List[str]):
        
        service = self.connect_to_api()

        start, end, reminders = self.parse_dates(start, end)

        attendees_ = [{"email": email} for email in attendees]

        inputs= {
            'summary': summary,
            'location': location,
            'description': description,
            'start': start,
            'end': end,
            'attendees': attendees_,
            'reminders': reminders
        }


        self.create_event(inputs, service)
        
        print('Event created successfully!')
   

        
class TimeAvailabilty(BaseModel):
    """Model for Time Availability"""
    start: Optional[str] = Field(..., description="Start date and time to check users availabilty")
    end: Optional[str] = Field(None, description="end date and time to check users availabilty")
 



class TimeAvailabilityTool(MeetingScedulerTool):
    """Tool to check users available time on the google calendar."""
    name: str = "check availabilty"
    description: str = "used for checking users available time on google calendar"
    args_schema: Type[BaseModel] = TimeAvailabilty





    def get_availability_for_range(self, start_date_str, end_date_str, service):
        # Parse strings to datetime objects
        start_time = datetime.strptime(start_date_str, "%B %d, %Y, %I:%M%p")
        end_time = datetime.strptime(end_date_str, "%B %d, %Y, %I:%M%p")

        # Get timezone
   
        local_zone = get_localzone()

        # Add timezone info
        start_time = start_time.replace(tzinfo=local_zone)
        end_time = end_time.replace(tzinfo=local_zone)

        available_days = []
        current_dt = start_time.date()
        end_date = end_time.date()

        while current_dt <= end_date:
            start_dt = datetime.combine(current_dt, datetime.min.time()).replace(tzinfo=local_zone)
            end_dt = datetime.combine(current_dt, datetime.max.time()).replace(tzinfo=local_zone)

            if start_dt < start_time:
                start_dt = start_time
            if end_dt > end_time:
                end_dt = end_time

            body = {
                "timeMin": start_dt.isoformat(),
                "timeMax": end_dt.isoformat(),
                "timeZone": str(local_zone),
                "items": [{"id": "primary"}]
            }

            result = service.freebusy().query(body=body).execute()
            busy_times = result['calendars']['primary'].get('busy', [])

            print(f"Querying for {current_dt}")
            print("Raw busy times:", busy_times)

            free_slots = []
            current_start = start_dt

            for period in busy_times:
                busy_start = datetime.fromisoformat(period['start']).astimezone(local_zone)
                busy_end = datetime.fromisoformat(period['end']).astimezone(local_zone)

                if busy_start > current_start:
                    free_slots.append((current_start.time().isoformat(), busy_start.time().isoformat()))
                current_start = max(current_start, busy_end)

            if current_start < end_dt:
                free_slots.append((current_start.time().isoformat(), end_dt.time().isoformat()))

            if free_slots:
                available_days.append({
                    "date": current_dt.isoformat(),
                    "available": free_slots
                })

            current_dt += timedelta(days=1)

        return available_days
    

    def _run(self, start, end):
        
        service = self.connect_to_api()

        available_days = self.get_availability_for_range(start, end, service)
 
        
        return available_days



class EventChecker(BaseModel):
    """Model for events checker"""
    start: Optional[str] = Field(..., description="Start date and time to check users availabilty")
    end: Optional[str] = Field(None, description="end date and time to check users availabilty")
 



class EventCheckerTool(MeetingScedulerTool):
    """Tool to check users events on the google calendar by using date provided."""
    name: str = "event checker"
    description: str = "used for checking users upcoming events on google calendar"
    args_schema: Type[BaseModel] = EventChecker




    def get_events(self, service, start, end=None):
        try:
            start_dt = datetime.strptime(start, "%B %d, %Y, %I:%M%p").date()
            
            end_dt = None
            if end:
                end_dt = datetime.strptime(end, "%B %d, %Y, %I:%M%p").date()

            print("Getting all upcoming events")

            page_token = None
            matched_events = []
            while True:
                events_result = service.events().list(calendarId='primary', pageToken=page_token).execute()
                for event in events_result.get('items', []):
                    event_start = event["start"].get("dateTime", event["start"].get("date"))

                    try:
                        event_start_dt = datetime.fromisoformat(event_start).date()
                    except ValueError:
                        print(f'Skipping event with invalid date format {event.get("summary", "Untitled")}')
                        continue

                    # Filter by start and end range if provided
                    if end_dt:
                        if not start_dt <= event_start_dt <= end_dt:
                            continue
                    else:
                        if event_start_dt < start_dt:
                            continue

                    # Matched event
                    event_summary = event.get('summary', 'No Title')
                    print(f"{event_start} - {event_summary}")
                    matched_events.append({
                        'start': event_start,
                        'summary': event_summary
                    })

                page_token = events_result.get('nextPageToken')
                if not page_token:
                    break

            if not matched_events:
                print("No upcoming events found.")
            return matched_events

        except Exception as error:
            print(f"An error occurred: {error}")

    
    def _run(self, start, end):
        service = self.connect_to_api()

        events = self.get_events(service, start, end)
        return events








