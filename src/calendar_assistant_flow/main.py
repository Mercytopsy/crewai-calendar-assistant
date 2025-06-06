import warnings

from datetime import datetime
from tzlocal import get_localzone
from typing import List
from crewai import Crew, Process

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from datetime import datetime
from tzlocal import get_localzone
from calendar_assistant_flow.crews.Manager_crew.manager_crew import ManagerServiceCrew
from calendar_assistant_flow.crews.Assistant_crew.assistant_crew import CalendarAssistant

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")




                
calendar_assistant = CalendarAssistant()

class CalendarState(BaseModel): 
    id: str = "1"
    question: str = "Can you help me check my availability and schedule a meeting with joe@gmail.com by 9pm today for daily standup."
    # question: str = "Can you help me check my avalability today."
    chosen_assistant: List[str] = []
    response: List[str] = []
    current_date: str =""

class CalendarAssistantFlow(Flow[CalendarState]):
    """The main workflow managing manager and assistant interactions."""
  
    initial_state = CalendarState

    
    @start()
    def execute_manager(self):
        """Starts the manager crew to decide which assistant(s) to engage."""
        
        print("Kickoff the Manager Crew")

        local_tz = get_localzone()
        current_date = str(datetime.now(local_tz).date())
        output = (
            ManagerServiceCrew()
            .crew()
            .kickoff(inputs={"question": self.state.question,
                             "current_date": current_date})
        )
      
        chosen_assistant = output["chosen_assistant"]
        print("Selected_assistant:", chosen_assistant)

        self.state.chosen_assistant = chosen_assistant
        self.state.current_date = current_date
        
        return chosen_assistant
    

    
    @listen(execute_manager)
    def assistant_crew(self):
        """Runs the relevant assistant crew(s) based on the manager's decision."""
        feedbacks: List[str] = []
        chosen_assistant = [str(name).strip() for name in self.state.chosen_assistant]

        
        print("Chosen assistants:", chosen_assistant)  # Debugging       
       
       # Map assistant names to their corresponding task methods
        available_assistant = {
        'meeting_scheduler_assistant': calendar_assistant.meeting_scheduler_assistant,
        'availability_checker_assistant': calendar_assistant.availability_checker_assistant,
        'event_checker_assistant': calendar_assistant.event_checker_assistant,
        }

 
        assistant_task_map = {
            "availability_checker_assistant": [calendar_assistant.dateinterpreter_task,calendar_assistant.availability_checker_task],
            "meeting_scheduler_assistant": [calendar_assistant.meeting_crafter_task, calendar_assistant.meeting_scheduler_task],
            "event_checker_assistant": [calendar_assistant.dateinterpreter_task, calendar_assistant.event_checker_task],
        }

        for assistant in chosen_assistant:
            selected_assistant = available_assistant.get(assistant)
            if not selected_assistant:
                print(f"No function found for assistant: {assistant}")
                continue

            agent_instance = selected_assistant()
            # Get the correct task(s) for this assistant
            task_functions = assistant_task_map.get(assistant, [])
            tasks = [task() for task in task_functions]

            if not tasks:
                print(f"No tasks defined for assistant: {assistant}")
                continue

            # Create crew with only relevant agent and task
            agent_crew = Crew(
                agents=[agent_instance],
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )

            output = agent_crew.kickoff(inputs={
                "question": self.state.question,
                "current_date": self.state.current_date
            })
            feedbacks.append(f"{assistant} stated: {output}")

        self.state.response = feedbacks
        
                        


    @listen(assistant_crew)
    def generate_client_response(self):
        """Collect all response from the assistants"""
        return self.state.response
    



def kickoff():
    """Entry point to start the flow."""
    flow = CalendarAssistantFlow()
    flow.kickoff()




if __name__ == "__main__":
    kickoff()



