from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.console import Group

def show_welcome():
    console = Console()
    
    # --- Header ---
    title = Text("🚀 TERMINUS AI", style="bold white", justify="center")
    subtitle = Text("Google Workspace Automation Service", style="cyan", justify="center")
    header = Group(title, subtitle, Text(""))

    # --- Commands Table ---
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta", expand=True, border_style="blue")
    table.add_column("Service", style="bold cyan", width=12)
    table.add_column("Example Command", style="green")

    # Add Rows
    table.add_row("📅 Calendar", 'terminus run "show my meetings"')
    table.add_row("", 'terminus run "schedule demo tomorrow at 10am"')
    table.add_section()
    
    table.add_row("📁 Drive", 'terminus run "list drive files"')
    table.add_row("", 'terminus run "create folder Demo_Folder"')
    table.add_section()

    table.add_row("📊 Sheets", 'terminus run "create sheet Budget_2026"')
    table.add_row("📄 Docs", 'terminus run "create document Project_Plan"')
    table.add_row("📝 Forms", 'terminus run "create feedback form Hackathon"')
    table.add_section()

    table.add_row("⚡ Workflow", 'terminus run "prepare project workspace Demo"')
    table.add_section()
    
    table.add_row("⏰ Scheduler", 'terminus scheduler-run')
    table.add_row("", 'terminus run "send daily email at 08:00"')

    # --- Footer ---
    footer = Text("\n💡 Tip: I understand natural language! Try 'read my emails' or 'plan my day'.", style="italic dim yellow", justify="center")

    # --- Main Panel ---
    main_panel = Panel(
        Group(header, table, footer),
        border_style="bright_blue",
        padding=(1, 2),
        title="[bold green]ACTIVE[/bold green]",
        subtitle="[bold]v1.0.0[/bold]"
    )
    
    console.print(main_panel)
    console.print("")
