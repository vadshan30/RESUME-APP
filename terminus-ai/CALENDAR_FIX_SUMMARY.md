# Calendar Query Fix - Summary

## Issue
The AI parser was not recognizing natural calendar queries like:
- "any meetings tomorrow"
- "tomorrow meeting" (singular)
- "upcoming meetings"

## Solution
Enhanced the regex patterns in `ai/parser.py` to support:

### 1. **Singular Forms**
- Changed `meetings` → `meeting|meetings`
- Changed `events` → `event|events`

### 2. **"Upcoming" Keyword**
- Added `upcoming` to the list of action verbs

### 3. **Standalone Queries**
- Added pattern to match just "meetings" or "events" without any prefix

## Updated Patterns

```python
# Calendar - List (BEFORE)
(r"(list|show|get|check|what is on).* (calendar|events|meetings|schedule)", "calendar", "list", None),

# Calendar - List (AFTER - 4 patterns)
(r"(any|list|show|get|check|what is on|what are|upcoming).* (meeting|meetings|event|events|calendar|schedule)", "calendar", "list", None),
(r"(tomorrow|today).* (meeting|meetings|event|events|schedule)", "calendar", "list", None),
(r"(meeting|meetings|event|events|schedule).* (tomorrow|today)", "calendar", "list", None),
(r"^(meeting|meetings|event|events)$", "calendar", "list", None),
```

## ✅ Now Working Commands

All these variations now work in assistant mode:

### Time-based Queries
- ✅ `any meetings tomorrow`
- ✅ `tomorrow meeting`
- ✅ `tomorrow meetings`
- ✅ `meetings tomorrow`
- ✅ `today events`
- ✅ `events today`

### Upcoming Queries
- ✅ `upcoming meetings`
- ✅ `upcoming events`
- ✅ `any upcoming meetings`
- ✅ `show upcoming events`

### Simple Queries
- ✅ `meetings`
- ✅ `events`
- ✅ `show my meetings`
- ✅ `list calendar events`
- ✅ `what are my meetings`

## Testing

Tested in both modes:
1. **Run mode**: `.\terminus.ps1 run "tomorrow meeting"` ✅
2. **Assistant mode**: `.\terminus.ps1 assistant` then type `any upcoming meetings` ✅

## Files Modified
- `ai/parser.py` - Enhanced calendar list regex patterns
- `AI_COMMANDS_REFERENCE.md` - Updated documentation with new examples

---
**Date:** 2026-02-14  
**Status:** ✅ FIXED
