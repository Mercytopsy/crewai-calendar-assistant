## 🧠 Calendar Multi-Agent Assistant with CrewAI

This project is a **multi-agent personal assistant for managing calendars and schedules**, built using [CrewAI](https://docs.crewai.com/). 

### 👥 Agents

This personal assistant consists of three specialized agents, each handling a core aspect of calendar management.

**📅 Meeting Scheduler Agent**  
- Handles the scheduling of new meetings.
- Understands time zones, meeting duration, participants, and context.
  
**🕒 Availability Checker Agent**  
- Checks user availability based on existing calendar events.
- Helps find optimal time slots for new meetings.
  
 **🎉 Event Checker Agent**  
- Reviews and retrieves details about existing calendar events.
- Can answer questions like “What do I have today?” or “Show me next week’s schedule.”

These agents are given tasks by a **Manager Agent** and structured within a unified **CrewAI Flow**.


### 🛠️ Tech Stack

- 🧠 [CrewAI](https://github.com/CrewAI/crewAI)
- 🐍 Python 3.10+
- LLms-GPT-4o model

### 🔗 Integrations

- **Google Calendar API** – for reading and writing events, checking availability, and syncing real user calendars.





### 🙋‍♀️ Why I Built This

I created this project as a demonstration of how **CrewAI** can be used to build **collaborative agent systems** tailored to real-world workflows like calendar management. It's designed for anyone who wants to experiment with LLM-powered task delegation in a practical domain.

