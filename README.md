## 🧠 Calendar Multi-Agent Assistant with CrewAI

This project is a **multi-agent personal assistant for managing calendars and schedules**, built using [CrewAI](https://docs.crewai.com/). The system orchestrates a collaborative set of specialized agents through a centralized **CrewAI Flow**, offering seamless automation of meeting scheduling, availability checking, and event tracking.

### 🚀 Overview

Designed to act as your intelligent calendar companion, this assistant is powered by three specialized CrewAI agents and a managing agent that coordinates their tasks. The system streamlines calendar-related tasks through a modular and extensible CrewAI architecture.

### 👥 Agents

- **📅 Meeting Scheduler Agent**  
  Proposes and schedules meetings based on user input, availability, and context.

- **🕒 Availability Checker Agent**  
  Scans calendar data or inputs to determine optimal times for new events or meetings.

- **🎉 Event Checker Agent**  
  Tracks existing events, ensures no overlaps, and provides quick summaries of upcoming events.

These agents are dynamically orchestrated by a **Manager Agent** using CrewAI's `@crew` method and structured within a unified **CrewAI Flow**.

### 🛠️ Tech Stack

- 🧠 [CrewAI](https://github.com/CrewAI/crewAI)
- 🐍 Python 3.10+
- Optional: LangChain, LLMs (OpenAI, Claude, etc.) depending on your agent logic

### 📦 Features

- Modular agent structure: easily extend or modify individual agents
- CrewAI Flow integration for seamless task coordination
- Human-like calendar management using AI agents
- Reusable architecture for other assistant-style tools

### 📸 Example Use Case

A user needs to schedule a new meeting. The system:
1. Uses the **Availability Checker Agent** to find free time slots
2. Confirms no conflicting events using the **Event Checker Agent**
3. Uses the **Meeting Scheduler Agent** to book and confirm the event


### 🚧 Future Improvements

- Google Calendar / Outlook API Integration
- Natural language interface (via Chat UI or CLI)
- Reminder and notification agent
- Time zone support

### 📄 License

This project is licensed under the MIT License.

---

### ✨ Contributions

Feel free to fork, contribute, or suggest improvements!

---

### 🙋‍♀️ Why I Built This

I created this project as a demonstration of how **CrewAI** can be used to build **collaborative agent systems** tailored to real-world workflows like calendar management. It's designed for anyone who wants to experiment with LLM-powered task delegation in a practical domain.

