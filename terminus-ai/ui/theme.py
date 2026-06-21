from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.console import Group
from rich.align import Align

console = Console()

class Theme:
    """
    Centralized theme management matching the user's preferred Blue/Green/Magenta aesthetic.
    """
    # Colors validating the user's screenshot
    COLOR_BORDER = "bright_blue"
    COLOR_TITLE_ACTIVE = "bold green"
    COLOR_TABLE_HEADER = "magenta"
    COLOR_COMMAND = "green"
    COLOR_SERVICE = "cyan"
    COLOR_TIP = "italic yellow"

    @staticmethod
    def print_welcome():
        """
        Prints the dashboard in the specific visual style requested.
        """
        # --- Header ---
        # Emoji + Title
        title_text = Text("🚀 TERMINUS AI", style="bold white", justify="center")
        subtitle_text = Text("Google Workspace Automation Service", style="bold blue", justify="center")
        header_group = Group(title_text, subtitle_text, Text(""))

        # --- Table ---
        table = Table(
            box=box.ROUNDED, 
            show_header=True, 
            header_style=Theme.COLOR_TABLE_HEADER, 
            expand=True, 
            border_style="blue",
            padding=(0, 1)
        )
        table.add_column("Service", style=f"bold {Theme.COLOR_SERVICE}", width=12)
        table.add_column("Example Command", style=Theme.COLOR_COMMAND)

        # --- Rows ---
        # Calendar
        table.add_row("📅 Calendar", 'terminus run "show my meetings"')
        table.add_row("", 'terminus run "schedule demo tomorrow at 10am"')
        table.add_section()
        
        # Drive
        table.add_row("📁 Drive", 'terminus run "list drive files"')
        table.add_row("", 'terminus run "create folder Demo_Folder"')
        table.add_section()

        # Mail
        table.add_row("📧 Mail", 'terminus run "send smart email"')
        table.add_row("", 'terminus run "organize my emails"')
        table.add_section()

        # Workspace
        table.add_row("📊 Sheets", 'terminus run "create sheet Budget_2026"')
        table.add_row("📄 Docs", 'terminus run "create document Project_Plan"')
        table.add_row("📝 Forms", 'terminus run "create feedback form Hackathon"')
        table.add_section()

        # Workflow
        table.add_row("⚡ Workflow", 'terminus run "prepare project workspace Demo"')
        table.add_section()
        
        # Scheduler
        table.add_row("⏰ Scheduler", 'terminus scheduler-run')
        table.add_row("", 'terminus run "send daily email at 08:00"')
        table.add_section()

        # TESTING COMMANDS (The new Master features, styled to fit)
        table.add_row("🔥 Testing", 'terminus run "execute smart workday"')
        table.add_row("", 'terminus run "create smart doc Topic"')
        table.add_row("", 'terminus assistant')

        # --- Footer ---
        footer_text = Text("\n💡 Tip: I understand natural language! Try 'read my emails' or 'plan my day'.", style=Theme.COLOR_TIP, justify="center")

        # --- Main Panel ---
        # "ACTIVE" title in Green, Blue border
        main_panel = Panel(
            Group(header_group, table, footer_text),
            box=box.ROUNDED,
            border_style=Theme.COLOR_BORDER,
            padding=(1, 2),
            title=f"[{Theme.COLOR_TITLE_ACTIVE}]ACTIVE[/{Theme.COLOR_TITLE_ACTIVE}]",
            subtitle="[bold white]v1.0.0[/bold white]"
        )
        
        console.print(main_panel)
        console.print("")

    @staticmethod
    def print_chatbot_welcome():
        """
        Prints the chatbot mode welcome panel.
        """
        chat_panel = Panel(
            "[bold cyan]🤖 AI CHATBOT MODE[/bold cyan]\n\n"
            "[white]I understand natural language! Just talk to me like you would a human assistant.[/white]\n\n"
            "[bold yellow]Try asking:[/bold yellow]\n"
            '  💬 "When is my next meeting?"\n'
            '  💬 "Explain tomorrow\'s meetings"\n'
            '  💬 "Summarize my last 5 emails"\n'
            '  💬 "Create a sheet called Q1 Revenue"\n'
            '  💬 "What files did I upload last week?"\n'
            '  💬 "Send the summary to my manager"\n\n'
            "[bold green]Commands:[/bold green]\n"
            "  • Type [bold]clear[/bold] to reset conversation history\n"
            "  • Type [bold]exit[/bold] or [bold]quit[/bold] to leave\n",
            title="[bold green]CHAT[/bold green]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        console.print(chat_panel)

    @staticmethod
    def print_briefing(calendar_events, emails):
        """
        Prints the Daily Briefing panel.
        """
        # Calendar Section
        cal_text = Text()
        if calendar_events:
            for e in calendar_events:
                cal_text.append(f"• {e['Time']}: {e['Event']}\n", style="cyan")
        else:
            cal_text.append("• No meetings today.\n", style="dim italic")

        # Email Section
        email_text = Text()
        if emails:
            for m in emails:
                email_text.append(f"• {m['Subject']} (From: {m['From']})\n", style="white")
        else:
            email_text.append("• Inbox is clear.\n", style="dim italic")
        
        # Suggested Actions
        actions_text = Text("• Review meeting notes\n• Clear Drive clutter\n", style="green")

        # Layout
        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_row(Panel(cal_text, title="📅 Meetings Today", border_style="cyan"))
        grid.add_row(Panel(email_text, title="📧 Important Emails", border_style="yellow"))
        grid.add_row(Panel(actions_text, title="⚡ Suggested Actions", border_style="green"))

        console.print(Panel(
            grid,
            title="[bold magenta]TODAY'S AI BRIEFING[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        ))
