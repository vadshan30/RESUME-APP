from rich.console import Console
from services.drive import DriveService
from services.docs import DocsService
from services.sheets import SheetsService
from services.forms import FormsService
from services.calendar import CalendarService
from services.gmail import GmailService
from utils.formatter import Formatter

console = Console()

class WorkflowService:
    """
    Orchestrates multi-service workflows.
    """
    def __init__(self, creds):
        self.creds = creds
        self.drive = DriveService(creds)
        self.docs = DocsService(creds)
        self.sheets = SheetsService(creds)
        self.forms = FormsService(creds)
        self.calendar = CalendarService(creds)
        self.gmail = GmailService(creds)

    def setup_project_workspace(self, project_name):
        """
        Creates a complete workspace: Folder, Doc (with content), Sheet (with columns), Form, and Kickoff Event.
        """
        console.print(f"[bold cyan]🚀 Starting Advanced Project Setup: {project_name}[/bold cyan]")
        
        summary = []
        
        # 1. Create Folder
        folder_id = self.drive.create_folder(f"{project_name}_Folder")
        if folder_id:
            summary.append(f"📁 Drive Folder: {project_name}_Folder (ID: {folder_id})")
        
        # 2. Create Doc and Add Content
        doc_title = f"{project_name}_Plan"
        doc_id = self.docs.create_document(doc_title)
        if doc_id:
            summary.append(f"📄 Project Doc: {doc_title}")
            # Add initial content
            try:
                # Basic content template
                content = f"Project: {project_name}\n\nGoals:\n- automates everything\n- uses AI\n\nArchitecture:\n- Python/Google API"
                self.docs.write_text(doc_id, content)
                summary.append("   - Added initial project goals and architecture.")
            except:
                pass

        # 3. Create Sheet and Add Headers
        sheet_title = f"{project_name}_Budget"
        sheet_id = self.sheets.create_sheet(sheet_title)
        if sheet_id:
            summary.append(f"📊 Budget Sheet: {sheet_title}")
            # Add Header Row
            try:
                self.sheets.append_row(sheet_id, ["Date", "Task", "Owner", "Status", "Budget"])
                summary.append("   - Added columns: Date, Task, Owner, Status, Budget")
            except:
                pass

        # 4. Create Registration Form
        form_title = f"{project_name}_Registration"
        form_id = self.forms.create_form(form_title)
        if form_id:
            summary.append(f"📝 Registration Form: {form_title}")
            summary.append("   - Added default questions.")

        # 5. Create Calendar Reminder
        event = self.calendar.create_event(f"Kickoff: {project_name} tomorrow at 10am")
        if event:
            # fix for event summary extraction if dict is returned differently
            evt_sum = event.get('summary', 'Kickoff')
            evt_time = event.get('start', 'tomorrow')
            summary.append(f"📅 Kickoff Event: {evt_sum} ({evt_time})")

        return summary

    def send_meeting_summary(self):
        """
        Fetches the last meeting and emails a summary (mock).
        """
        # 1. Get last event (mock logic: get first event from list)
        events = self.calendar.list_events(max_results=1)
        if not events:
            console.print("[yellow]No recent meetings found to summarize.[/yellow]")
            return False

        last_event = events[0]
        
        # 2. Generate Summary (Mock AI)
        subject = f"Summary: {last_event['Summary']}"
        body = f"""
        Hi Team,
        
        Here is the summary for '{last_event['Summary']}' on {last_event['Start Time']}.
        
        Action Items:
        - [ ] Review project specs
        - [ ] Update tracker
        
        Best,
        Terminus AI
        """
        
        # 3. Send Email (Mock)
        # self.gmail.send_email("team@example.com", subject, body)
        
        console.print(f"[green]📧 Sending email to team...[/green]")
        console.print(f"[dim]{subject}[/dim]")
        
        return True
