from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from rich.console import Console
import os

console = Console()

class DriveService:
    """
    Service for interacting with Google Drive API.
    """
    def __init__(self, creds):
        self.service = build('drive', 'v3', credentials=creds)

    def list_files(self, page_size=10):
        """
        Fetches files from Google Drive.
        """
        try:
            console.print("[cyan]Fetching Drive files...[/cyan]")
            results = self.service.files().list(
                pageSize=page_size, fields="nextPageToken, files(id, name, mimeType)").execute()
            items = results.get('files', [])

            if not items:
                console.print("[yellow]No files found.[/yellow]")
                return []

            formatted_files = []
            for item in items:
                formatted_files.append({
                    "Name": item['name'],
                    "ID": item['id'],
                    "Type": item['mimeType']
                })
            
            return formatted_files

        except Exception as e:
            console.print(f"[bold red]Error fetching files: {e}[/bold red]")
            return []

    def upload_file(self, file_path):
        """
        Uploads a file to Google Drive.
        """
        if not os.path.exists(file_path):
            console.print(f"[bold red]Error: File '{file_path}' not found.[/bold red]")
            return

        file_name = os.path.basename(file_path)
        try:
            console.print(f"[cyan]Uploading '{file_name}'...[/cyan]")
            file_metadata = {'name': file_name}
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            console.print(f"[bold green]File Uploaded! ID: {file.get('id')}[/bold green]")
            return file.get('id')
            
        except Exception as e:
            console.print(f"[bold red]Error uploading file: {e}[/bold red]")
            return None

    def create_folder(self, folder_name):
        """
        Creates a new folder in Google Drive.
        """
        try:
            console.print(f"[cyan]Creating folder '{folder_name}'...[/cyan]")
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            file = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            console.print(f"[bold green]Folder Created! ID: {file.get('id')}[/bold green]")
            return file.get('id')
            
        except Exception as e:
            console.print(f"[bold red]Error creating folder: {e}[/bold red]")
            return None
