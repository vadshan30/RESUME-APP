from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED, MINIMAL
from rich.text import Text
from rich import print as rprint

console = Console()

class Formatter:
    """
    Handles rich output formatting for the CLI.
    """
    @staticmethod
    def print_table(title, columns, rows):
        """
        Prints a rich table with styling.
        """
        table = Table(title=f"[bold cyan]{title}[/bold cyan]", box=ROUNDED, show_lines=True)
        
        colors = ["cyan", "magenta", "green", "yellow", "blue"]
        
        for i, col in enumerate(columns):
            color = colors[i % len(colors)]
            table.add_column(col, style=color, justify="left" if i == 0 else "center")
            
        for row in rows:
            table.add_row(*[str(item) for item in row])
            
        console.print(table)
        console.print()

    @staticmethod
    def print_panel(content, title="Info", style="blue"):
        """
        Prints a styled panel.
        """
        console.print(Panel(
            content,
            title=f"[bold {style}]{title}[/bold {style}]",
            border_style=style,
            box=ROUNDED,
            padding=(1, 2)
        ))

    @staticmethod
    def print_success(message):
        rprint(f"[bold green]✔ {message}[/bold green]")

    @staticmethod
    def print_error(message):
        rprint(f"[bold red]✘ {message}[/bold red]")
        
    @staticmethod
    def print_header():
        """
        Prints the main application header (Now redundant with new Welcome Screen, keeping minimal).
        """
        pass # Skip header on every command to reduce noise, since we have a welcome screen now.
