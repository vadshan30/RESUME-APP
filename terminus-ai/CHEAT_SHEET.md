# 🚀 TERMINUS AI - Command Cheat Sheet

## 📌 STEP 1: Start the AI Assistant

Open PowerShell in the project folder and run:

```powershell
.\terminus assistant
```

You'll see:
```
TERMINUS AI >
```

---

## 📌 STEP 2: Type Your Commands

Now just type naturally! Here are the most useful commands:

### 📅 CALENDAR COMMANDS

```
tomorrow meeting
any upcoming meetings
show my meetings
plan my day
schedule meeting with John tomorrow at 3pm
```

### 📊 CREATE SHEETS

```
create sheet Budget_2026
create sheet Task_Tracker
create smart sheet Budget
```

### 📄 CREATE DOCUMENTS

```
create document Project_Plan
create smart doc Marketing_Strategy
```

### 📁 DRIVE COMMANDS

```
list drive files
create folder Hackathon_2026
upload demo.txt
```

### 📧 EMAIL COMMANDS

```
read my emails
list 5 emails
send smart email
organize my emails
```

### 🧠 SMART AI FEATURES

```
daily briefing
prepare next meeting
execute smart workday
build workflow
```

### 💬 OTHER

```
hello
exit
```

---

## 🎯 QUICK EXAMPLES

### Example 1: Check Your Day
```powershell
PS> .\terminus assistant

TERMINUS AI > plan my day
# Shows your schedule

TERMINUS AI > any upcoming meetings
# Lists meetings

TERMINUS AI > exit
```

### Example 2: Create Project Resources
```powershell
PS> .\terminus assistant

TERMINUS AI > create folder NewProject
# Creates folder

TERMINUS AI > create smart doc Project_Plan
# Creates AI-generated document

TERMINUS AI > create smart sheet Task_Tracker
# Creates AI-generated sheet

TERMINUS AI > exit
```

### Example 3: Morning Routine
```powershell
PS> .\terminus assistant

TERMINUS AI > daily briefing
# Shows calendar + emails + suggestions

TERMINUS AI > prepare next meeting
# Creates meeting notes doc

TERMINUS AI > exit
```

---

## ⚡ SINGLE COMMAND MODE

If you just want to run ONE command without entering assistant mode:

```powershell
.\terminus run "tomorrow meeting"
.\terminus run "create sheet Budget"
.\terminus run "plan my day"
```

---

## 🔧 TROUBLESHOOTING

### If commands don't work after code changes:

```powershell
.\clear_cache.ps1
```

Then try again!

---

## 💡 REMEMBER

1. ✅ **DO**: Use `.\terminus assistant` then type commands
2. ✅ **DO**: Use `.\terminus run "command"` for single commands
3. ❌ **DON'T**: Type commands directly in PowerShell without `terminus`

---

**Need the full list?** Check `AI_COMMANDS_REFERENCE.md`
