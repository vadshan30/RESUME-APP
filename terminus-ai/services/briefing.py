from services.calendar import CalendarService
from services.gmail import GmailService
from services.docs import DocsService
from ui.theme import Theme
from rich.console import Console

console = Console()

class BriefingService:
    """
    Aggregates data across services to generate intelligent briefings and reports.
    """
    def __init__(self, creds):
        self.creds = creds
        self.calendar = CalendarService(creds)
        self.gmail = GmailService(creds)
        self.docs = DocsService(creds)

    def generate_daily_briefing(self):
        """
        Aggregates today's events and emails.
        """
        # Get Daily Plan (Reuse Calendar Logic)
        plan = self.calendar.get_daily_plan() # Defaults to tomorrow, need to fix arg
        
        # Get Recent Emails
        emails = self.gmail.list_messages(max_results=3)

        Theme.print_briefing(plan['events'] if plan else [], emails)
        return True

    def prepare_next_meeting(self):
        """
        Finds the next meeting and creates a notes document.
        """
        events = self.calendar.list_events(max_results=1)
        if not events:
            console.print("[yellow]No upcoming meetings found.[/yellow]")
            return None

        next_event = events[0]
        title = next_event["Summary"]
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip()
        doc_title = f"Notes: {safe_title}"
        
        # Create Doc
        doc_id = self.docs.create_document(doc_title)
        
        if doc_id:
            # Add Template
            content = f"Meeting: {title}\nTime: {next_event['Start Time']}\n\n1. Goals\n\n2. Discussion\n\n3. Action Items"
            self.docs.write_text(doc_id, content)
            return {"title": doc_title, "id": doc_id}
        
        
        return None

    def organize_emails(self):
        """
        Simulates intelligent email organization for demonstration.
        """
        try:
            # 1. Fetch unread (using existing list_messages)
            messages = self.gmail.list_messages(max_results=10)
            
            if not messages:
                return ["✅ Inbox is clean! No unread emails found."]

            # 2. Mock Analysis
            important = []
            updates = []
            others = []

            for msg in messages:
                subject = msg['Subject']
                subject_lower = subject.lower()
                
                if any(k in subject_lower for k in ["urgent", "meeting", "deadline", "important", "alert"]):
                    important.append(f"• {subject}")
                elif any(k in subject_lower for k in ["update", "report", "info", "status", "newsletter"]):
                    updates.append(f"• {subject}")
                else:
                    others.append(f"• {subject}")

            report = []
            if important:
                report.append("[bold red]🚨 IMPORTANT:[/bold red]")
                report.extend(important)
                report.append("")
            
            if updates:
                report.append("[bold blue]ℹ️ UPDATES:[/bold blue]")
                report.extend(updates)
                report.append("")

            if others:
                report.append("[dim]📂 OTHERS:[/dim]")
                report.extend(others)
                
            if not report:
                report.append("Inbox analyzed. Nothing critical found.")
                
            return report

        except Exception as e:
            return [f"⚠️ Unable to organize emails right now: {str(e)}"]

    def send_digest(self):
        """
        Generates and sends a daily digest email to the user.
        """
        try:
            # 1. Get Data
            plan = self.calendar.get_daily_plan()
            emails = self.gmail.list_messages(max_results=5)
            
            # 2. Compose Body
            body = "Here is your Daily Digest:\n\n📅 Agenda:\n"
            if plan and plan.get('events'):
                for e in plan['events']:
                    body += f"- {e['Time']}: {e['Event']}\n"
            else:
                body += "- No meetings today.\n"
                
            body += "\n📧 Top Unread Emails:\n"
            if emails:
                for m in emails:
                    body += f"- {m['Subject']} (From: {m['From']})\n"
            else:
                body += "- Inbox clear.\n"
            
            # 3. Send (Mock)
            # In a real app: self.gmail.send_email("me", "Daily Digest", body)
            return body
        except Exception as e:
            return f"Error generating digest: {str(e)}"
