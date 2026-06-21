# TERMINUS AI - Complete Natural Language Commands Reference

## 🤖 How to Use
Run the assistant in interactive mode:
```powershell
.\terminus assistant
```

Or run a single command:
```powershell
.\terminus run "your command here"
```

---

## 📅 CALENDAR COMMANDS

### List Events
- `show my meetings`
- `list calendar events`
- `what is on my calendar`
- `check my schedule`
- `get calendar events`
- `any meetings tomorrow` ✨
- `tomorrow meetings` ✨
- `tomorrow meeting` ✨ (singular)
- `meetings today` ✨
- `today events` ✨
- `what are my meetings` ✨
- `any upcoming meetings` ✨
- `upcoming meetings` ✨
- `upcoming events` ✨
- Just type: `meetings` or `events` ✨

### Plan Your Day
- `plan my day`
- `plan for today`
- `agenda for tomorrow`
- `schedule my day`

### Create Events
- `schedule meeting with CEO tomorrow at 10am`
- `create meeting tomorrow at 5pm`
- `set up appointment next Monday at 2pm`
- `add event Team Standup on Friday at 9am`

---

## 📁 GOOGLE DRIVE COMMANDS

### List Files
- `list my drive files`
- `show drive files`
- `get files`

### Upload Files
- `upload requirements.txt`
- `upload demo.txt`
- `upload <filename>`

### Create Folders
- `create folder Hackathon_Project_2026`
- `make folder Demo_Folder`
- `create directory NewProject`

---

## 📧 GMAIL COMMANDS

### List Emails
- `read my emails`
- `list gmail messages`
- `show emails`
- `get emails`
- `read 5 emails` (specify number)
- `list 10 messages`

---

## 📄 GOOGLE DOCS COMMANDS

### Create Document
- `create document Project_Plan`
- `make doc Meeting_Notes`
- `create doc Proposal`

### Read Document
- `read document <document_id>`
- `show doc <document_id>`
- `get document <document_id>`

---

## 📊 GOOGLE SHEETS COMMANDS

### Create Sheet
- `create sheet Budget_2026`
- `make spreadsheet Task_Tracker`
- `create sheet top 10 laptops`

### Append Row (Advanced)
- `add row to <sheet_id> with values <data>`
- `append line to <sheet_id> values <data>`

---

## 📝 GOOGLE FORMS COMMANDS

### Create Form
- `create form Hackathon_Feedback`
- `make survey Customer_Survey`
- `create form Registration`

### Read Form
- `read form <form_id>`
- `show form <form_id>`
- `get form <form_id>`

---

## 🧠 SMART AI FEATURES (Advanced)

### Smart Document Generation
- `create smart doc Marketing_Strategy`
- `generate smart document Project_Roadmap`
- `make smart doc Quarterly_Review`

**What it does:** Creates a structured document with AI-generated sections (Executive Summary, Objectives, Implementation Plan, Timeline, Conclusion)

### Smart Sheet Generation
- `create smart sheet Budget`
- `generate smart spreadsheet Task_Tracker`
- `make smart sheet Event_Planning`

**What it does:** Creates a sheet with intelligent headers and sample data based on keywords:
- **Budget** → Category, Item, Cost, Owner, Status
- **Task/Tracker** → Task ID, Task Name, Assignee, Priority, Due Date, Status
- **Event** → Time, Activity, Location, Responsible, Notes

### Smart Email Composer
- `send smart email`
- `compose smart mail`

**What it does:** Interactive email composer with AI-generated content based on purpose and tone

### Build Workflow
- `build workflow`
- `create pipeline`

**What it does:** Interactive project setup wizard (creates docs, sheets, and meetings)

### Master Workday Automation
- `execute smart workday`
- `run master automation`

**What it does:** Full morning routine - briefing + meeting notes + optimization

---

## 📋 BRIEFING & AUTOMATION COMMANDS

### Daily Briefing
- `daily briefing`
- `morning summary`
- `daily status`

**What it does:** Shows calendar events, important emails, and suggested actions

### Prepare for Next Meeting
- `prepare next meeting`
- `setup upcoming meeting`
- `get ready for next event`

**What it does:** Creates a Google Doc with meeting agenda and notes template

### Organize Emails
- `organize my emails`
- `cleanup emails`
- `sort emails`

**What it does:** AI categorizes emails (urgent, important, promotional, spam)

### Send Daily Digest
- `send daily digest`
- `email morning summary`
- `send daily email summary`

**What it does:** Emails you a summary of your day

---

## ⚡ WORKFLOW COMMANDS

### Project Workspace Setup
- `prepare project workspace Demo`
- `setup project NewApp`
- `create project workspace Hackathon`

**What it does:** Creates folder, doc, sheet, and kickoff meeting for a project

### Meeting Summary
- `send meeting summary to team`
- `email meeting notes to everyone`

**What it does:** Sends meeting notes to team members

### Workday Automation
- `start workday automation`
- `begin workday`
- `run day automation`

**What it does:** Morning briefing + meeting prep

---

## ⏰ SCHEDULER COMMANDS

### Schedule Daily Email
- `send daily email at 08:00`
- `schedule email summary at 09:30`

**What it does:** Sets up recurring daily email digest

---

## 💬 GENERAL COMMANDS

### Greeting
- `hello`
- `hi`
- `hey`

---

## 🎯 COMMAND EXAMPLES BY USE CASE

### Starting Your Day
```
daily briefing
plan my day
prepare next meeting
```

### Managing Projects
```
prepare project workspace NewFeature
create smart doc Project_Plan
create smart sheet Task_Tracker
```

### Quick Tasks
```
show my meetings
create folder Q1_Reports
upload presentation.pdf
read my emails
```

### Advanced Automation
```
execute smart workday
build workflow
organize my emails
send daily digest
```

---

## 📝 NOTES

1. **Natural Language**: The AI parser understands variations of these commands
2. **Case Insensitive**: Commands work in any case
3. **Flexible Phrasing**: You don't need exact matches - the AI extracts intent
4. **Arguments**: Replace `<placeholders>` with actual values

## 🚀 Pro Tips

- Use **assistant mode** for interactive sessions: `.\terminus assistant`
- Use **run mode** for single commands: `.\terminus run "command"`
- Commands with "smart" prefix use AI-generated content
- Most commands open the created resource in your browser automatically

---

**Version:** 1.0.0  
**Last Updated:** February 14, 2026
