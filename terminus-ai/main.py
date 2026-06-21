import typer
import webbrowser
from rich.console import Console
from rich.panel import Panel
from auth.auth import GoogleAuth
from services.calendar import CalendarService
from services.drive import DriveService
from services.gmail import GmailService
from services.docs import DocsService
from services.forms import FormsService
from services.sheets import SheetsService
from services.scheduler import SchedulerService
from services.workflow import WorkflowService
from services.briefing import BriefingService
from services.smart import SmartService
from ai.parser import AIParser
from ai.chatbot import ChatbotEngine
from utils.formatter import Formatter
from ui.theme import Theme

app = typer.Typer()
console = Console()

def print_banner():
    """Prints the CLI banner."""
    Formatter.print_header()

@app.command()
def hello():
    """
    Test command to verify CLI is working.
    """
    print_banner()
    console.print("[bold green]Welcome to TERMINUS AI CLI![/bold green]")

@app.command()
def login():
    """
    Authenticate with Google Workspace.
    """
    print_banner()
    console.print("[yellow]Initiating Login Flow...[/yellow]")
    auth = GoogleAuth()
    creds = auth.authenticate()
    if creds:
        Formatter.print_success("Successfully logged in via Google OAuth!")
    else:
        Formatter.print_error("Login failed. Check your internet or credentials.")

@app.command()
def calendar(action: str = typer.Argument(..., help="Action to perform: list")):
    """
    Manage Google Calendar events.
    """
    print_banner()
    auth = GoogleAuth()
    creds = auth.authenticate()
    if not creds:
        console.print("[red]Login required.[/red]")
        return

    service = CalendarService(creds)

    if action.lower() == "list":
        events = service.list_events()
        if events:
            Formatter.print_table("Upcoming Events", ["Summary", "Start Time", "Link"], 
                                  [[e["Summary"], e["Start Time"], e["Link"]] for e in events])
    else:
        console.print(f"[red]Unknown action: {action}[/red]")

@app.command()
def drive(
    action: str = typer.Argument(..., help="Action: list, upload, create-folder"),
    argument: str = typer.Argument(None, help="File path or Folder name (optional)")
):
    """
    Manage Google Drive files and folders.
    """
    print_banner()
    auth = GoogleAuth()
    creds = auth.authenticate()
    if not creds:
        console.print("[red]Login required.[/red]")
        return

    service = DriveService(creds)

    if action.lower() == "list":
        files = service.list_files()
        if files:
            Formatter.print_table("Recent Files", ["Name", "ID", "Type"], 
                                  [[f["Name"], f["ID"], f["Type"]] for f in files])

    elif action.lower() == "upload":
        if not argument:
            console.print("[red]Error: Please provide a file path to upload.[/red]")
            return
        service.upload_file(argument)

    elif action.lower() == "create-folder":
        if not argument:
            console.print("[red]Error: Please provide a folder name.[/red]")
            return
        service.create_folder(argument)
    
    else:
        console.print(f"[red]Unknown action: {action}[/red]")

def execute_intent(creds, result):
    """
    Executes the command based on the parsed result.
    """
    service_name = result["service"]
    action = result["action"]
    argument = result["argument"]
    confidence = result.get("confidence", 0.0)

    if confidence < 0.5:
        Formatter.print_error("I'm not sure what you mean.")
        console.print("[dim]Try: 'list calendar events', 'upload file.txt', or 'create folder NewProject'[/dim]")
        return False

    Formatter.print_panel(f"Service: [bold]{service_name.upper()}[/bold]\nAction: [bold]{action.upper()}[/bold]\nTarget: {argument if argument else 'N/A'}", title="Intent Detected", style="green")

    if service_name == "calendar":
        if action == "list":
            with console.status("[bold green]Fetching Calendar Events...[/bold green]", spinner="dots"):
                service = CalendarService(creds)
                events = service.list_events()
            
            if events:
                Formatter.print_table("Upcoming Events", ["Summary", "Start Time", "Link"], 
                                      [[e["Summary"], e["Start Time"], e["Link"]] for e in events])
            else:
                 Formatter.print_panel("No upcoming events found.", title="Calendar", style="yellow")
        
        elif action == "create":
            if argument:
                with console.status("[bold green]Scheduling Event...[/bold green]", spinner="clock"):
                    service = CalendarService(creds)
                    result = service.create_event(argument)
                
                if result:
                    Formatter.print_success(f"Event Scheduled: {result['summary']}")
                    console.print(f"[bold cyan]Time:[/bold cyan] {result['start']}")
                    console.print(f"[link={result['link']}][bold blue]👉 Click here to open in Google Calendar[/bold blue][/link]")
                    webbrowser.open(result['link'])
            else:
                Formatter.print_error("Missing event details (e.g., 'tomorrow at 5pm').")
        
        elif action == "plan":
             with console.status("[bold green]Creating Daily Plan...[/bold green]", spinner="dots"):
                service = CalendarService(creds)
                plan = service.get_daily_plan()
            
             if plan:
                Formatter.print_panel(f"Date: {plan['date']}\n\n[bold]Agenda:[/bold]", title="Daily Planner", style="cyan")
                if plan['events']:
                    Formatter.print_table("Schedule", ["Time", "Event"], 
                                          [[e["Time"], e["Event"]] for e in plan['events']])
                else:
                    console.print("[italic]No events scheduled. Full free day![/italic]")
                console.print(Panel("\n".join(plan['free_slots']), title="Suggested Focus Blocks", border_style="green"))

    elif service_name == "scheduler":
        service = SchedulerService(creds)
        if action == "email_digest":
            if argument:
                success = service.add_daily_email_summary(argument)
                if success:
                    Formatter.print_success(f"Daily Email Digest scheduled for {argument}")
                    console.print("[dim]Use 'python main.py scheduler run' to start the daemon process.[/dim]")
            else:
                 Formatter.print_error("Missing time (e.g. 08:00).")

    elif service_name == "drive":
        service = DriveService(creds)
        if action == "list":
            with console.status("[bold green]Fetching Drive Files...[/bold green]", spinner="dots"):
                files = service.list_files()
            
            if files:
                Formatter.print_table("Recent Files", ["Name", "ID", "Type"], 
                                      [[f["Name"], f["ID"], f["Type"]] for f in files])
            else:
                Formatter.print_panel("No files found in Drive.", title="Drive", style="yellow")

        elif action == "upload":
            if argument:
                with console.status(f"[bold green]Uploading {argument}...[/bold green]", spinner="arrow3"):
                    file_id = service.upload_file(argument)
                if(file_id):
                     Formatter.print_success(f"File uploaded successfully! ID: {file_id}")
            else:
                Formatter.print_error("Missing file path for upload.")

        elif action == "create-folder":
            if argument:
                with console.status(f"[bold green]Creating folder {argument}...[/bold green]", spinner="arrow3"):
                    folder_id = service.create_folder(argument)
                if(folder_id):
                     Formatter.print_success(f"Folder created successfully! ID: {folder_id}")
            else:
                Formatter.print_error("Missing folder name.")

    elif service_name == "gmail":
        service = GmailService(creds)
        if action == "list":
            max_results = 10
            if argument and argument.isdigit():
                max_results = int(argument)
            
            with console.status(f"[bold green]Fetching last {max_results} Emails...[/bold green]", spinner="dots"):
                messages = service.list_messages(max_results=max_results)
            
            if messages:
                Formatter.print_table("Recent Emails", ["From", "Subject", "ID"], 
                                      [[m["From"], m["Subject"], m["ID"]] for m in messages])
            else:
                Formatter.print_panel("No emails found.", title="Gmail", style="yellow")

    elif service_name == "docs":
        service = DocsService(creds)
        if action == "get":
            if argument:
                with console.status(f"[bold green]Fetching Document {argument}...[/bold green]", spinner="dots"):
                    doc = service.get_document(argument)
                if doc:
                    Formatter.print_panel(f"Title: {doc['Title']}\nID: {doc['ID']}", title="Google Doc", style="blue")
            else:
                 Formatter.print_error("Missing document ID.")
        elif action == "create":
            if argument:
                with console.status(f"[bold green]Creating Document {argument}...[/bold green]", spinner="dots"):
                    doc_id = service.create_document(argument)
                if doc_id:
                    url = f"https://docs.google.com/document/d/{doc_id}/edit"
                    Formatter.print_success(f"Document Created: [bold]{argument}[/bold]")
                    console.print(f"[link={url}][bold blue]👉 Open Document[/bold blue][/link]")
                    webbrowser.open(url)
            else:
                Formatter.print_error("Missing document title.")

    elif service_name == "sheets":
        service = SheetsService(creds)
        if action == "create":
            if argument:
               with console.status(f"[bold green]Creating Sheet {argument}...[/bold green]", spinner="dots"):
                   sheet_id = service.create_sheet(argument)
               if sheet_id:
                   url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
                   Formatter.print_success(f"Sheet Created: [bold]{argument}[/bold]")
                   console.print(f"[link={url}][bold blue]👉 Open Sheet[/bold blue][/link]")
                   webbrowser.open(url)
            else:
                Formatter.print_error("Missing sheet title.")

    elif service_name == "forms":
        service = FormsService(creds)
        if action == "get":
            if argument:
                with console.status(f"[bold green]Fetching Form {argument}...[/bold green]", spinner="dots"):
                    form = service.get_form(argument)
                if form:
                    Formatter.print_panel(f"Title: {form['Title']}\nID: {form['ID']}", title="Google Form", style="magenta")
            else:
                 Formatter.print_error("Missing form ID.")
        elif action == "create":
            if argument:
                with console.status(f"[bold green]Creating Form {argument}...[/bold green]", spinner="dots"):
                    form_id = service.create_form(argument)
                if form_id:
                    url = f"https://docs.google.com/forms/d/{form_id}/edit"
                    Formatter.print_success(f"Form Created: {form_id}")
                    console.print(f"[link={url}][bold blue]👉 Open Form[/bold blue][/link]")
                    webbrowser.open(url)
            else:
                Formatter.print_error("Missing form title.")

    elif service_name == "workflow":
        wf = WorkflowService(creds)
        if action == "project_setup":
            if argument:
                summary = wf.setup_project_workspace(argument)
                if summary:
                    Formatter.print_panel("\n".join(summary), title="Project Workspace Ready", style="green")
            else:
                 Formatter.print_error("Missing project name.")
        elif action == "meeting_summary":
            wf.send_meeting_summary()
            Formatter.print_success("Meeting summary sent to team!")
        elif action == "workday_automation":
            console.print("[bold cyan]🚀 Starting Workday Automation Sequence...[/bold cyan]")
            bs = BriefingService(creds)
            bs.generate_daily_briefing()
            res = bs.prepare_next_meeting()
            if res:
                  url = f"https://docs.google.com/document/d/{res['id']}/edit"
                  Formatter.print_success(f"Meeting Notes Ready: {res['title']}")
                  webbrowser.open(url)
            Formatter.print_panel("Workday Initialized Successfully", title="Automation Complete", style="green")

    elif service_name == "briefing":
        bs = BriefingService(creds)
        if action == "daily_briefing":
             with console.status("[bold green]Generating Briefing...[/bold green]", spinner="dots"):
                 bs.generate_daily_briefing()
        elif action == "prepare_meeting":
             with console.status("[bold green]Preparing Meeting Docs...[/bold green]", spinner="dots"):
                 res = bs.prepare_next_meeting()
             if res:
                 url = f"https://docs.google.com/document/d/{res['id']}/edit"
                 Formatter.print_success(f"Meeting Notes Created: [bold]{res['title']}[/bold]")
                 console.print(f"[link={url}][bold blue]👉 Open Notes[/bold blue][/link]")
                 webbrowser.open(url)
             else:
                 Formatter.print_panel("No upcoming meetings to prepare for.", title="Info", style="yellow")
        
        elif action == "organize_emails":
             with console.status("[bold green]🤖 AI Organizing Inbox...[/bold green]", spinner="dots"):
                 report = bs.organize_emails()
             Formatter.print_panel("\n".join(report), title="Email Organization Report", style="cyan")
             
        elif action == "send_digest":
             with console.status("[bold green]📧 Sending Daily Digest...[/bold green]", spinner="dots"):
                 body = bs.send_digest()
             Formatter.print_success("Daily Digest Email Sent!")
             console.print(Panel(body, title="Email Preview", border_style="dim"))

    elif service_name == "smart":
        smart = SmartService(creds)
        if action == "smart_doc":
            if argument:
                with console.status(f"[bold magenta]🧠 AI Generating Document: {argument}...[/bold magenta]", spinner="earth"):
                    res = smart.create_smart_document(argument)
                if res:
                    url = f"https://docs.google.com/document/d/{res['id']}/edit"
                    Formatter.print_success(f"Smart Doc Created: [bold]{res['title']}[/bold]")
                    console.print(f"[link={url}][bold blue]👉 Open Document[/bold blue][/link]")
                    webbrowser.open(url)
            else:
                Formatter.print_error("Missing topic.")
        elif action == "smart_sheet":
             if argument:
                with console.status(f"[bold magenta]🧠 AI Architecture Sheet: {argument}...[/bold magenta]", spinner="earth"):
                    res = smart.create_smart_sheet(argument)
                if res:
                    url = f"https://docs.google.com/spreadsheets/d/{res['id']}/edit"
                    Formatter.print_success(f"Smart Sheet Created: [bold]{res['title']}[/bold]")
                    console.print(f"[link={url}][bold blue]👉 Open Sheet[/bold blue][/link]")
                    webbrowser.open(url)
             else:
                Formatter.print_error("Missing purpose.")
        elif action == "smart_email":
            smart.compose_and_send_email()
        elif action == "build_workflow":
            summary = smart.build_workflow_interactive()
            if summary:
                Formatter.print_panel("\n".join(summary), title="Workflow Created", style="green")
        elif action == "smart_workday":
             console.print("[bold cyan]🚀 Executing Master Workday Protocol...[/bold cyan]")
             bs = BriefingService(creds)
             bs.generate_daily_briefing()
             res = smart.create_smart_document("Daily_Meeting_Notes")
             if res:
                 url = f"https://docs.google.com/document/d/{res['id']}/edit"
                 Formatter.print_success("Daily Notes Generated")
                 webbrowser.open(url)
             Formatter.print_panel("System Optimized. You are ready.", title="Master Automation", style="magenta")

    elif service_name == "general":
        if action == "hello":
            Formatter.print_panel("Hello! How can I help you manage your Google Workspace today?", title="Assistant", style="green")
    
    return True

@app.command()
def run(command: str):
    """
    Process a natural language command.
    """
    print_banner()
    auth = GoogleAuth()
    creds = auth.authenticate()
    if not creds:
        console.print("[red]Login required.[/red]")
        return

    parser = AIParser()
    result = parser.parse(command)
    execute_intent(creds, result)

@app.command()
def assistant():
    """
    Enter interactive AI assistant mode — conversational chatbot powered by OpenAI.
    Talk naturally: ask questions, give commands, or just chat!
    """
    Theme.print_chatbot_welcome()
    
    auth = GoogleAuth()
    creds = auth.authenticate()
    if not creds:
        console.print("[red]Login required.[/red]")
        return

    # Initialize chatbot engine
    chatbot = ChatbotEngine()
    
    if not chatbot.available:
        # Fall back to regex-based assistant if OpenAI is not available
        console.print("[yellow]⚠ Falling back to command-based mode (OpenAI not available).[/yellow]")
        parser = AIParser()
        allowed_services = {"calendar", "sheets", "drive", "briefing", "gmail", "docs", "forms", "smart", "workflow", "scheduler", "general"}
        
        while True:
            user_input = console.input("[bold magenta]TERMINUS AI > [/bold magenta]")
            if user_input.lower() in ["exit", "quit", "bye"]:
                console.print("[bold green]👋 Goodbye! See you next time.[/bold green]")
                break
            if not user_input.strip():
                continue
            result = parser.parse(user_input)
            service = result.get("service", "unknown")
            if service == "unknown" or service not in allowed_services:
                console.print("[yellow]⚠️  I didn't understand that. Try something like 'show my meetings' or 'check mail'.[/yellow]")
                continue
            execute_intent(creds, result)
        return

    # ─── Chatbot Mode ─────────────────────────────────────────────
    console.print()
    
    while True:
        try:
            user_input = console.input("[bold magenta]You > [/bold magenta]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold green]👋 Goodbye![/bold green]")
            break
        
        if user_input.lower().strip() in ["exit", "quit", "bye"]:
            console.print("[bold green]👋 Goodbye! Have a productive day! 🚀[/bold green]")
            break

        if user_input.lower().strip() == "clear":
            chatbot.clear_history()
            console.print("[dim]Conversation history cleared.[/dim]")
            continue

        if not user_input.strip():
            continue

        # Send to chatbot engine
        with console.status("[bold cyan]🤖 Thinking...[/bold cyan]", spinner="dots"):
            response = chatbot.chat(user_input)
    
        if response["mode"] == "action":
            # Execute the Google Workspace action
            intent = response["intent"]
            execute_intent(creds, intent)
        
        elif response["mode"] == "chat":
            # Display conversational response
            console.print(Panel(
                response["response"],
                title="[bold cyan]🤖 TERMINUS AI[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            ))
        
        elif response["mode"] == "error":
            console.print(Panel(
                response["response"],
                title="[bold red]⚠ Error[/bold red]",
                border_style="red",
                padding=(1, 2)
            ))
        
        elif response["mode"] == "fallback":
            # OpenAI quota exceeded — try regex parser as fallback
            fallback_parser = AIParser()
            fallback_result = fallback_parser.parse(user_input)
            if fallback_result.get("service") != "unknown":
                execute_intent(creds, fallback_result)
            else:
                console.print(Panel(
                    "OpenAI is currently unavailable (quota exceeded) and I couldn't match your command offline.\n\n"
                    "[bold yellow]Try simpler commands like:[/bold yellow]\n"
                    '  • "show my meetings"\n'
                    '  • "check mail"\n'
                    '  • "list drive files"\n'
                    '  • "create sheet Budget"\n'
                    '  • "plan my day"',
                    title="[bold yellow]⚠ Offline Mode[/bold yellow]",
                    border_style="yellow",
                    padding=(1, 2)
                ))
        
        console.print()


@app.command(name="ai")
def ai():
    """
    Alias for `assistant` to support `terminus ai` usage.
    """
    assistant()


@app.command(name="scheduler-run")
def scheduler_run():
    """
    Start the scheduler loop to run pending scheduled jobs.
    """
    print_banner()
    auth = GoogleAuth()
    creds = auth.authenticate()
    if not creds:
        console.print("[red]Login required.[/red]")
        return

    service = SchedulerService(creds)
    console.print("[bold yellow]Starting scheduler (Ctrl+C to stop)...[/bold yellow]")
    service.run_pending()

if __name__ == "__main__":
    from ui.welcome import show_welcome
    import sys
    
    # Show welcome only if not running the scheduler daemon to keep logs clean
    # and maybe if arguments are not empty (to avoid showing it when just piping)
    # The requirement says "When user runs .\terminus run 'command', welcome screen appears first"
    if "scheduler-run" not in sys.argv:
        Theme.print_welcome()
        
    # If no command is provided, exit gracefully after showing the welcome screen
    # This prevents Typer/Click from processing and showing "Missing command" error
    if len(sys.argv) == 1:
        sys.exit(0)

    app()
