from services.calendar import CalendarService
from services.gmail import GmailService
from services.docs import DocsService
from services.sheets import SheetsService
from services.drive import DriveService
from ui.theme import Theme
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

class SmartService:
    """
    Advanced AI Workspace Agent capabilities.
    Generates intelligent content, orchestrates workflows, and manages collaboration.
    """
    def __init__(self, creds):
        self.creds = creds
        self.calendar = CalendarService(creds)
        self.gmail = GmailService(creds)
        self.docs = DocsService(creds)
        self.sheets = SheetsService(creds)
        self.drive = DriveService(creds)

    def create_smart_document(self, topic):
        """Generates a structured document based on a topic."""
        console.print(f"[cyan]🧠 Analyzing topic: {topic}...[/cyan]")
        
        # Simulated AI Content Generation
        content = f"""
        # Project: {topic}
        
        ## 1. Executive Summary
        This document outlines the strategic initiatives for {topic}. It aims to streamline operations and enhance productivity using AI-driven workflows.
        
        ## 2. Objectives
        - Automate routine tasks.
        - Improve data accessibility.
        - Foster seamless collaboration.
        
        ## 3. Implementation Plan
        - **Phase 1:** Requirement Analysis
        - **Phase 2:** Development & Integration
        - **Phase 3:** Testing & Deployment
        
        ## 4. Timeline
        - Q1: Planning
        - Q2: Execution
        - Q3: Review
        
        ## 5. Conclusion
        By adopting this approach, we expect significant efficiency gains.
        """
        
        doc_id = self.docs.create_document(f"{topic}_Plan")
        if doc_id:
            self.docs.write_text(doc_id, content)
            return {"title": f"{topic}_Plan", "id": doc_id}
        return None

    def create_smart_sheet(self, purpose):
        """Generates a sheet with intelligent headers based on purpose."""
        console.print(f"[cyan]🧠 Analyzing purpose: {purpose}...[/cyan]")
        
        headers = ["Date", "Description", "Status"] # Default
        
        if "budget" in purpose.lower():
            headers = ["Date", "Category", "Item", "Cost", "Owner", "Status"]
            row_data = ["2026-02-14", "Software", "Hosting", "50.00", "Admin", "Paid"]
        elif "task" in purpose.lower() or "tracker" in purpose.lower():
            headers = ["Task ID", "Task Name", "Assignee", "Priority", "Due Date", "Status"]
            row_data = ["T-101", "Init Repo", "Dev", "High", "2026-02-20", "Done"]
        elif "event" in purpose.lower():
            headers = ["Time", "Activity", "Location", "Responsible", "Notes"]
            row_data = ["10:00 AM", "Registration", "Lobby", "Team A", "Check badges"]
        else:
            row_data = ["-", "-", "-"]

        sheet_id = self.sheets.create_sheet(f"{purpose}_Tracker")
        if sheet_id:
            self.sheets.append_row(sheet_id, headers)
            self.sheets.append_row(sheet_id, row_data)
            return {"title": f"{purpose}_Tracker", "id": sheet_id}
        return None

    def compose_and_send_email(self):
        """Interactively composes and sends an email."""
        console.print("[bold magenta]📧 Smart Email Composer[/bold magenta]")
        
        recipient = Prompt.ask("To (email)")
        purpose = Prompt.ask("Purpose (e.g. meeting, update)")
        tone = Prompt.ask("Tone", choices=["professional", "friendly", "urgent"], default="professional")
        
        # Simulated AI Generation
        subject = f"[{tone.title()}] {purpose.title()} Update"
        body = f"""
        Hello,
        
        I am writing to share an update regarding {purpose}. 
        
        Key Points:
        - We are making good progress.
        - Next steps are defined.
        
        Please let me know if you have any questions.
        
        Best regards,
        Terminus AI
        """
        
        console.print(Panel(body, title=f"Preview: {subject}", border_style="blue"))
        
        if Confirm.ask("Send this email?"):
            res = self.gmail.send_email(recipient, subject, body)
            if res:
                console.print(f"[green]✔ Email sent to {recipient}! (ID: {res['id']})[/green]")
                return True
            else:
                return False
        else:
            console.print("[yellow]Email cancelled.[/yellow]")
            return False

    def build_workflow_interactive(self):
        """Interactively builds a project workflow."""
        console.print("[bold cyan]🚀 AI Workflow Builder[/bold cyan]")
        
        project_name = Prompt.ask("Project Name")
        need_doc = Confirm.ask("Create Plan Document?")
        need_sheet = Confirm.ask("Create Tracker Sheet?")
        need_meeting = Confirm.ask("Schedule Kickoff Meeting?")
        
        summary = []
        
        if need_doc:
            res = self.create_smart_document(project_name)
            if res: summary.append(f"📄 Doc: {res['title']}")
            
        if need_sheet:
            res = self.create_smart_sheet(f"{project_name}_Tasks")
            if res: summary.append(f"📊 Sheet: {res['title']}")
            
        if need_meeting:
            event = self.calendar.create_event(f"Kickoff: {project_name} tomorrow at 10am")
            if event: summary.append(f"📅 Meeting: {event['summary']}")
            
        return summary
