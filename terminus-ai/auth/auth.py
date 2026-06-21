import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from rich.console import Console

console = Console()

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/forms.body.readonly'
]

class GoogleAuth:
    """
    Handles Google OAuth2 authentication flow.
    """
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.creds = None

    def authenticate(self):
        """
        Authenticates the user and returns credentials.
        """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_path):
            try:
                self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            except Exception as e:
                console.print(f"[red]Error loading token.json: {e}[/red]")
                self.creds = None

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # Retry logic for token refresh to handle transient network/SSL errors
                import time
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        console.print(f"[yellow]Refreshing expired token (Attempt {attempt+1}/{max_retries})...[/yellow]")
                        self.creds.refresh(Request())
                        break  # Success, exit loop
                    except Exception as e:
                        if attempt < max_retries - 1:
                            console.print(f"[red]Refresh failed: {e}. Retrying in 2s...[/red]")
                            time.sleep(2)
                        else:
                            console.print(f"[red]Error refreshing token after {max_retries} attempts: {e}. Re-authenticating...[/red]")
                            self.creds = None
            
            if not self.creds:
                if not os.path.exists(self.credentials_path):
                    console.print(f"[bold red]Error: '{self.credentials_path}' not found![/bold red]")
                    console.print("[yellow]Please download your OAuth 2.0 Client credentials from Google Cloud Console[/yellow]")
                    console.print(f"[yellow]and save them as '{self.credentials_path}' in the project root.[/yellow]")
                    return None

                console.print("[cyan]Initiating Google OAuth2 flow...[/cyan]")
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    # Use a fixed port to avoid random port assignment issues
                    self.creds = flow.run_local_server(port=8080, open_browser=True)
                except Exception as e:
                    console.print(f"[bold red]Authentication failed: {e}[/bold red]")
                    return None

            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())
                console.print("[green]Token saved to 'token.json'[/green]")

        return self.creds

if __name__ == "__main__":
    auth = GoogleAuth()
    creds = auth.authenticate()
    if creds:
        console.print("[bold green]Authentication successful![/bold green]")
