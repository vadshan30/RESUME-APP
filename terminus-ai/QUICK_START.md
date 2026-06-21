# TERMINUS AI - Quick Start Guide

## 🚀 How to Run Commands

### ❌ WRONG - Don't type commands directly in PowerShell
```powershell
tomorrow meeting          # This won't work!
any upcoming meetings     # This won't work!
```

### ✅ CORRECT - Use one of these methods:

---

## Method 1: Single Command Mode

Use `terminus run` followed by your command in quotes:

```powershell
.\terminus run "tomorrow meeting"
.\terminus run "any upcoming meetings"
.\terminus run "create sheet Budget_2026"
.\terminus run "show my meetings"
```

**When to use:** Quick one-off commands

---

## Method 2: Interactive Assistant Mode (RECOMMENDED)

Start the assistant, then type commands naturally:

```powershell
.\terminus assistant
```

Then you'll see the prompt:
```
TERMINUS AI >
```

Now you can type commands WITHOUT quotes:
```
tomorrow meeting
any upcoming meetings
create sheet Budget_2026
plan my day
exit
```

**When to use:** Multiple commands in a session

---

## Method 3: Direct Commands (Limited)

Some commands have direct shortcuts:

```powershell
.\terminus login
.\terminus calendar list
.\terminus drive list
```

**When to use:** Simple, non-AI commands

---

## 📝 Examples

### Example Session 1: Check Calendar
```powershell
PS> .\terminus run "any meetings tomorrow"
# Shows your calendar events
```

### Example Session 2: Interactive Mode
```powershell
PS> .\terminus assistant

TERMINUS AI > tomorrow meeting
# Shows calendar

TERMINUS AI > create sheet Budget_2026
# Creates a smart budget sheet

TERMINUS AI > plan my day
# Shows daily schedule

TERMINUS AI > exit
# Exits assistant mode
```

---

## 🎯 Key Points

1. **Natural language commands** only work through:
   - `.\terminus run "command"`
   - `.\terminus assistant` (then type commands)

2. **Don't type natural language directly in PowerShell** - PowerShell will try to execute them as programs

3. **Use quotes** with `terminus run` for multi-word commands

4. **No quotes needed** inside assistant mode

---

## 🔧 Setup Reminder

Make sure you're in the project directory:
```powershell
cd C:\Users\vadsh\OneDrive\vadshan\terminus-ai
```

Activate virtual environment (optional):
```powershell
.\venv\Scripts\Activate.ps1
```

---

## 📚 See Also

- `AI_COMMANDS_REFERENCE.md` - Full list of supported commands
- `DEMO.md` - Demo script for presentations
- `ARCHITECTURE.md` - Technical details
