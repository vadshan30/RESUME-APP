# TERMINUS AI CLI - Hackathon Demo Script

## 1. Introduction (30 Seconds)
"Judge, have you ever felt overwhelmed switching between Gmail, Calendar, and Drive?
Meet **TERMINUS AI** - your unified command-line interface for Google Workspace.
Instead of clicking through 10 tabs, I can manage my entire digital life with natural language commands."

## 2. Live Demo (2 Minutes)
*Run these commands in order. Make sure your terminal is visible and font is large.*

### A. Authentication
"First, we authenticate securely using OAuth 2.0."
```powershell
python main.py login
```
*(If already logged in, just mention: "I'm already authenticated securely via Google OAuth.")*

### B. Calendar Management
"Let's see my schedule for the day."
```powershell
python main.py run "show my calendar events"
```
*Point out the nice table formatting.*

### C. File Management (Drive)
"I need to find a specific file in my Drive."
```powershell
python main.py run "list my drive files"
```

"Now, let's automate a common task: creating a project folder."
```powershell
python main.py run "create folder Hackathon_Project_2026"
```

"And uploading our requirements file to it."
*(Upload a real file just to show it works)*
```powershell
python main.py run "upload requirements.txt"
```

### D. Email & Communication (Gmail)
"Finally, let's check for important updates without opening the browser."
```powershell
python main.py run "read my emails"
# OR
python main.py run "list gmail messages"
```

## 3. The "Wow" Factor (AI Parsing)
"The best part is the AI parser. I don't need to remember complex syntax. I just type:"
*Type this casually*
```powershell
python main.py run "hello"
```

## 4. Closing (30 Seconds)
"TERMINUS AI is built with Python, Typer, and Rich, and uses the official Google APIs.
It's extensible, fast, and brings the power of the cloud to your terminal.
Thank you!"
