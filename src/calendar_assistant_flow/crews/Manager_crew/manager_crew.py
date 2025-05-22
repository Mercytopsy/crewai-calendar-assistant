from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

from dotenv import load_dotenv


from calendar_assistant_flow.models import  AgentSelection


import os

load_dotenv()





api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_API_BASE")




@CrewBase
class ManagerServiceCrew():
    """CalendarManager crew"""

    agents_config= 'config/agents.yaml'
    task_config = 'config/tasks.yaml'



    llm = LLM(
		model="openai/gpt-4o",
		api_key=os.getenv("OPENAI_API_KEY"),
	)
    
  


    @agent
    def project_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['project_manager'],
            verbose=True,
            llm=self.llm
        )
    
   
    @task
    def project_manager_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_manager_task'],
            output_pydantic=AgentSelection
            
        )
    
  
    @crew
    def crew(self) -> Crew:
        """Creates the Managers crew"""
  
        return Crew(
            agents= self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
 
        )
