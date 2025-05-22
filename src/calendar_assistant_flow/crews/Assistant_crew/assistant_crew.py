from crewai import Agent, Crew, Task, LLM
from crewai.project import CrewBase, agent, task
from dotenv import load_dotenv


from calendar_assistant_flow.tools.custom_tool import MeetingScedulerTool, TimeAvailabilityTool, EventCheckerTool
from calendar_assistant_flow.models import DateInterpreter, MeetingCrafter


import os
load_dotenv()




api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_API_BASE")







@CrewBase
class CalendarAssistant():
    """CalendarAssistant crew"""

    agents_config= 'config/agents.yaml'
    task_config = 'config/tasks.yaml'



   

 

    llm = LLM(
		model="openai/gpt-4o",
		api_key=os.getenv("OPENAI_API_KEY"),
	)
    
  
  

    
    @agent
    def meeting_scheduler_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['meeting_scheduler_assistant'],
            verbose=True,
            tools=[MeetingScedulerTool()],
            llm=self.llm
        )

    @agent
    def datetime_interpreter_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['datetime_interpreter_specialist'], 
            verbose=True,
            llm=self.llm
        
        )
	
    @agent
    def availability_checker_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['availability_checker_assistant'], 
            verbose=True,
            tools=[TimeAvailabilityTool()],
            llm=self.llm
            
        )

    @agent
    def event_checker_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['event_checker_assistant'],
            verbose=True,
            tools=[EventCheckerTool()],
            llm=self.llm
        )
    

  
    @task
    def meeting_crafter_task(self) -> Task:
        return Task(
            config=self.tasks_config['meeting_crafter_task'],
            output_pydantic=MeetingCrafter
            
        )

    @task
    def meeting_scheduler_task(self) -> Task:
        return Task(
            config=self.tasks_config['meeting_scheduler_task']         
        )
   
    @task
    def dateinterpreter_task(self) -> Task:
        return Task(
            config=self.tasks_config['dateinterpreter_task'], 
            output_pydantic=DateInterpreter
         
        )
	
    @task
    def availability_checker_task(self) -> Task:
        return Task(
            config=self.tasks_config['availability_checker_task'], 
            output_file='report.md'
           
        )
    
    @task
    def event_checker_task(self) -> Task:
        return Task(
            config=self.tasks_config['event_checker_task'], 
            output_file='report.md'
        )
	
