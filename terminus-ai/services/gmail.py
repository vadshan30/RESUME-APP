from googleapiclient.discovery import build
import base64
from email.utils import parsedate_to_datetime
from rich.console import Console

console = Console()

class GmailService:
    """
    Service for interacting with Gmail API.
    """
    def __init__(self, creds):
        self.service = build('gmail', 'v1', credentials=creds)

    def list_messages(self, max_results=10):
        """
        Fetches emails from inbox.
        """
        try:
            console.print("[cyan]Fetching Gmail messages...[/cyan]")
            results = self.service.users().messages().list(userId='me', maxResults=max_results).execute()
            messages = results.get('messages', [])

            if not messages:
                console.print("[yellow]No messages found.[/yellow]")
                return []

            formatted_messages = []
            for msg in messages:
                msg_detail = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                headers = msg_detail['payload']['headers']
                
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown)')
                
                formatted_messages.append({
                    "From": sender,
                    "Subject": subject,
                    "ID": msg['id']
                })
            
            return formatted_messages

        except Exception as e:
            console.print(f"[bold red]Error fetching emails: {e}[bold red]")
            return []

    def send_email(self, recipient, subject, body):
        """
        Sends an email.
        """
        try:
            message = {
                'raw': base64.urlsafe_b64encode(
                    f"To: {recipient}\r\n"
                    f"Subject: {subject}\r\n\r\n"
                    f"{body}".encode("utf-8")
                ).decode("utf-8")
            }
            
            console.print(f"[cyan]Sending email to {recipient}...[/cyan]")
            result = self.service.users().messages().send(userId="me", body=message).execute()
            return result
        except Exception as e:
            console.print(f"[bold red]Error sending email: {e}[/bold red]")
            return None
