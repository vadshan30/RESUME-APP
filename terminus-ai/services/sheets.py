from googleapiclient.discovery import build
from rich.console import Console

console = Console()

class SheetsService:
    """
    Service for interacting with Google Sheets API.
    """
    def __init__(self, creds):
        self.service = build('sheets', 'v4', credentials=creds)

    def create_sheet(self, title):
        """Creates a new Google Sheet and populates it with starter data."""
        try:
            console.print(f"[cyan]Creating Sheet '{title}'...[/cyan]")
            spreadsheet_body = {'properties': {'title': title}}
            spreadsheet = self.service.spreadsheets().create(body=spreadsheet_body, fields='spreadsheetId').execute()
            sheet_id = spreadsheet.get('spreadsheetId')
            console.print(f"[green]Sheet Created! ID: {sheet_id}[/green]")
            
            # Generate Smart Content
            self._insert_starter_data(sheet_id, title)
            
            return sheet_id
        except Exception as e:
            console.print(f"[bold red]Error creating sheet: {e}[/bold red]")
            return None

    def _insert_starter_data(self, sheet_id, sheet_name):
        """Inserts headers and example rows based on the sheet name."""
        name_lower = sheet_name.lower()
        
        if "budget" in name_lower:
            data = [
                ["Category", "Description", "Estimated Cost", "Actual Cost", "Status"],
                ["Development", "API usage and cloud services", "200", "0", "Planned"],
                ["Marketing", "Promotion and outreach", "150", "0", "Planned"],
                ["Infrastructure", "Hosting and storage", "100", "0", "Planned"],
                ["Hardware", "Devices and peripherals", "500", "450", "Purchased"]
            ]
        elif "task" in name_lower or "tracker" in name_lower:
            data = [
                ["Task", "Owner", "Priority", "Deadline", "Status"],
                ["Design CLI interface", "Team Lead", "High", "2026-02-20", "In Progress"],
                ["Integrate Google APIs", "Backend Dev", "High", "2026-02-22", "Pending"],
                ["Build AI Parser", "AI Dev", "Medium", "2026-02-23", "Pending"],
                ["Documentation", "Writer", "Low", "2026-02-28", "Not Started"]
            ]
        else:
            data = [
                ["Date", "Topic", "Discussion", "Action Items", "Owner"],
                ["2026-02-14", "Initial Setup", "Environment and Auth", "Finish logic", "Admin"]
            ]

        try:
            body = {'values': data}
            # Use columns and rows starting from A1
            range_name = f"Sheet1!A1"
            self.service.spreadsheets().values().update(
                spreadsheetId=sheet_id, range=range_name,
                valueInputOption="USER_ENTERED", body=body).execute()
            
            # Optional: Formatting headers (Bold)
            self._format_header(sheet_id)
            
            console.print(f"[green]Smart data initialized in Sheet {sheet_id}[/green]")
        except Exception as e:
            console.print(f"[yellow]Failed to populate sheet data: {e}[/yellow]")

    def _format_header(self, sheet_id):
        """Formats the first row of a sheet as bold."""
        try:
            requests = [{
                'repeatCell': {
                    'range': {
                        'sheetId': 0, # Assuming first sheet
                        'startRowIndex': 0,
                        'endRowIndex': 1
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {'bold': True}
                        }
                    },
                    'fields': 'userEnteredFormat.textFormat.bold'
                }
            }]
            self.service.spreadsheets().batchUpdate(spreadsheetId=sheet_id, body={'requests': requests}).execute()
        except:
            pass # Silently fail formatting if sheetId != 0 or other issues

    def append_row(self, sheet_id, values):
        """Appends a row of values to the sheet."""
        try:
            body = {'values': [values]}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=sheet_id, range="A1",
                valueInputOption="USER_ENTERED", body=body).execute()
            console.print(f"[green]Row appended to Sheet {sheet_id}[/green]")
            return result
        except Exception as e:
            console.print(f"[bold red]Error appending row: {e}[/bold red]")
            return None

    def read_sheet(self, sheet_id, range_name="A1:E10"):
        """Reads values from a sheet."""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=sheet_id, range=range_name).execute()
            rows = result.get('values', [])
            return rows
        except Exception as e:
            console.print(f"[bold red]Error reading sheet: {e}[/bold red]")
            return []
