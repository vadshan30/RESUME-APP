from rich.console import Console
import re
from ai.openai_parser import OpenAIParser

console = Console()

class AIParser:
    """
    Parses natural language commands to identify intent and parameters.
    Uses OpenAI API when available, falls back to Regex patterns.
    """
    def __init__(self):
        # Try to initialize OpenAI parser
        self.openai_parser = OpenAIParser()
        
        # Define patterns for various intents (fallback)
        self.patterns = [
            # Gmail - Check first because it includes "check" which can conflict with Calendar patterns
            (r"^(check|list).*(mail|email|messages)$", "gmail", "list", None),
            (r"(check|list)\s+(last|recent)?\s*(mail|email|messages)", "gmail", "list", None),
            (r"(read|list|show|get|check).* (\d+) (emails|messages|mail|gmail)", "gmail", "list", "quantity"),
            (r"(read|list|show|get|check).* (emails|messages|mail|gmail)", "gmail", "list", None),
            (r"(summarize|summary).* (\d+) (emails|messages|mail)", "gmail", "list", "quantity"),
            (r"(summarize|summary).* (emails|messages|mail)", "gmail", "list", None),
            (r"(what|any) .*(new|unread|recent) (email|mail|message)", "gmail", "list", None),
            (r"(inbox|mailbox)", "gmail", "list", None),
            
            # Master AI Features
            (r"(create|make|generate) smart (doc|document) (.*)", "smart", "smart_doc", "topic"),
            (r"(create|make|generate) smart (sheet|spreadsheet) (.*)", "smart", "smart_sheet", "purpose"),
            (r"(send|compose) smart (email|mail)", "smart", "smart_email", None),
            (r"(build|create) (workflow|pipeline)", "smart", "build_workflow", None),
            (r"(execute|run) (smart|master) (workday|automation)", "smart", "smart_workday", None),

            # Advanced Features
            (r"(daily|morning) (briefing|summary|status)", "briefing", "daily_briefing", None),
            (r"(prepare|setup|get ready for) (next|upcoming) (meeting|event)", "briefing", "prepare_meeting", None),
            (r"(organize|cleanup|sort) (my )?emails", "briefing", "organize_emails", None),
            (r"(send|email) (daily|morning) (mail|email)? ?(summary|digest)", "briefing", "send_digest", None),
            (r"(start|begin|run) (workday|day|automation)", "workflow", "workday_automation", None),
            (r"assistant", "general", "assistant_mode", None),

            # Workflows
            (r"(prepare|setup|create).* (project|workspace) (.*)", "workflow", "project_setup", "project_name"),
            (r"(send|email).* (meeting|event) (summary|notes).* (team|everyone)", "workflow", "meeting_summary", None),

            # Schedule Planner — EXPANDED for natural language
            (r"(plan|agenda|schedule) (my|for) (tomorrow|today|day)", "calendar", "plan", "date_ref"),
            (r"what.* (my|today).* (plan|agenda|schedule)", "calendar", "plan", None),
            (r"(today|tomorrow).* (plan|agenda|schedule)", "calendar", "plan", "date_ref"),
            (r"(plan|agenda) .*(today|tomorrow)", "calendar", "plan", "date_ref"),
            (r"what.* plan .*(today|tomorrow)", "calendar", "plan", "date_ref"),

            # Daily Email Scheduler
            (r"(send|schedule).* (daily|email|summary).* at (\d{1,2}:\d{2})", "scheduler", "email_digest", "time"),

            # Calendar - List — EXPANDED for natural language
            (r"(any|list|show|get|check|what is on|what are|upcoming).* (meeting|meetings|event|events|calendar|schedule)", "calendar", "list", None),
            (r"(tomorrow|today).* (meeting|meetings|event|events|schedule)", "calendar", "list", None),
            (r"(meeting|meetings|event|events|schedule).* (tomorrow|today)", "calendar", "list", None),
            (r"^(meeting|meetings|event|events)$", "calendar", "list", None),
            (r"when.* (my|next|upcoming) (meeting|event|appointment)", "calendar", "list", None),
            (r"when.* meeting", "calendar", "list", None),
            (r"(what|tell|explain|describe).* (tomorrow|today).* meeting", "calendar", "list", None),
            (r"(explain|describe|tell me about).* meeting", "calendar", "list", None),
            (r"(do i have|any).* meeting.* (today|tomorrow|this week)", "calendar", "list", None),
            (r"(what|anything).* (on|for) (my )?(calendar|schedule)", "calendar", "list", None),
            (r"(next|upcoming) (meeting|event|appointment)", "calendar", "list", None),
            (r"(my|today|tomorrow).* (calendar|schedule)", "calendar", "list", None),
            
            # Calendar - Create
            (r"(schedule|set up|create|add).* (meeting|event|appointment) (.*)", "calendar", "create", "details"),
            (r"^schedule (.*)", "calendar", "create", "details"),
            
            # Drive - Files — EXPANDED
            (r"(list|show|get).* (files|drive)", "drive", "list", None),
            (r"(what|which) files.* (upload|have|recent|last)", "drive", "list", None),
            (r"(my|recent) (files|documents|drive)", "drive", "list", None),
            (r"(upload) (.*)", "drive", "upload", "file_path"),
            
            # Drive - Folders
            (r"(create|make).* (folder|directory) (.*)", "drive", "create-folder", "folder_name"),
            
            # Sheets
            (r"(create|make).* (sheet|spreadsheet) (.*)", "sheets", "create", "title"),
            (r"(add|append).* (row|line) to (.*) (with values|values) (.*)", "sheets", "append", "details"),
            
            # Docs
            (r"(create|make).* (doc|document) (.*)", "docs", "create", "title"),
            (r"(write|append).* to (doc|document) (.*) (content|text) (.*)", "docs", "write", "details"),

            # Forms
            (r"(create|make).* (form|survey) (.*)", "forms", "create", "title"),
            
            # Docs - Read
            (r"(read|show|get).* (doc|document) (.*)", "docs", "get", "document_id"),

            # Forms - Read
            (r"(read|show|get).* (form) (.*)", "forms", "get", "form_id"),
            
            # Greeting — EXPANDED
            (r"(hello|hi|hey|good morning|good evening|good afternoon)", "general", "hello", None),
            (r"(help|what can you do|how do you work)", "general", "hello", None),
            (r"(thank|thanks|thank you)", "general", "hello", None),
        ]

    def parse(self, text):
        """
        Extracts service, action, and arguments from text.
        Tries OpenAI API first, falls back to regex patterns.
        """
        text = text.lower().strip()
        console.print(f"[dim]Parsing: '{text}'[/dim]")

        # Try OpenAI parser first
        if self.openai_parser.openai_available:
            openai_result = self.openai_parser.parse(text)
            if openai_result:
                return openai_result
            # If OpenAI fails, fall through to regex

        # Fallback to regex patterns
        for pattern, service, action, arg_name in self.patterns:
            match = re.search(pattern, text)
            if match:
                argument = None
                if arg_name:
                    # Extracts the group corresponding to the argument
                    # e.g., "upload file.txt" -> match.group(2) is "file.txt"
                    try:
                        argument = match.group(match.lastindex).strip()
                    except:
                        argument = None
                
                return {
                    "service": service,
                    "action": action,
                    "argument": argument,
                    "confidence": 1.0
                }

        return {"service": "unknown", "action": "unknown", "argument": None, "confidence": 0.0}
