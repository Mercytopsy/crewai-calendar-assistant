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

### 🔗 Connect to Google Calendar API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. **Enable Google Calendar API**:
   - Navigate to `APIs & Services > Library`
   - Search for **Google Calendar API** and click **Enable**
4. **Configure OAuth consent screen**:
   - Go to `APIs & Services > OAuth consent screen`
   - Select user type and complete the required fields
5. **Create OAuth Client ID**:
   - Go to `APIs & Services > Credentials`
   - Click **Create Credentials > OAuth client ID**
   - Choose **Desktop app** as the application type
   - Click **Create**
6. **Download the JSON file** and rename it to:
   ```bash
   credentials.json

### 📦 Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/repo-name.git
cd repo-name
add credentials.json downloaded
crewai install

### 🚀 Run the Assistant
- crewai flow kickoff



