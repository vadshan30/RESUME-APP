from googleapiclient.discovery import build
from rich.console import Console

console = Console()

class FormsService:
    """
    Service for interacting with Google Forms API.
    """
    def __init__(self, creds):
        self.service = build('forms', 'v1', credentials=creds)

    def get_form(self, form_id):
        """Fetches form details."""
        try:
            console.print(f"[cyan]Fetching Form {form_id}...[/cyan]")
            form = self.service.forms().get(formId=form_id).execute()
            title = form.get('info', {}).get('title', 'Untitled Form')
            console.print(f"[green]Found Form: {title}[/green]")
            return {"Title": title, "ID": form_id}
        except Exception as e:
            console.print(f"[bold red]Error fetching form: {e}[/bold red]")
            return None

    def create_form(self, title):
        """Creates a new form with default questions."""
        try:
            console.print(f"[cyan]Creating Form '{title}'...[/cyan]")
            form_body = {
                "info": {
                    "title": title,
                }
            }
            form = self.service.forms().create(body=form_body).execute()
            form_id = form.get('formId')
            
            # Add default questions
            update_body = {
                "requests": [
                    {
                        "createItem": {
                            "item": {
                                "title": "How would you rate your experience?",
                                "questionItem": {
                                    "question": {
                                        "required": True,
                                        "scaleQuestion": {
                                            "low": 1,
                                            "high": 5,
                                            "lowLabel": "Poor",
                                            "highLabel": "Excellent"
                                        }
                                    }
                                }
                            },
                            "location": {"index": 0}
                        }
                    },
                    {
                        "createItem": {
                            "item": {
                                "title": "Any feedback?",
                                "questionItem": {
                                    "question": {
                                        "required": False,
                                        "textQuestion": {}
                                    }
                                }
                            },
                            "location": {"index": 1}
                        }
                    }
                ]
            }
            self.service.forms().batchUpdate(formId=form_id, body=update_body).execute()
            
            console.print(f"[green]Form Created! ID: {form_id}[/green]")
            return form_id
        except Exception as e:
            console.print(f"[bold red]Error creating form: {e}[/bold red]")
            return None
