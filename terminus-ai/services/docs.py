from googleapiclient.discovery import build
from rich.console import Console

console = Console()

class DocsService:
    """
    Service for interacting with Google Docs API.
    """
    def __init__(self, creds):
        self.service = build('docs', 'v1', credentials=creds)

    def create_document(self, title):
        """Creates a new Google Doc and populates it with starter content."""
        try:
            console.print(f"[cyan]Creating Document '{title}'...[/cyan]")
            body = {'title': title}
            doc = self.service.documents().create(body=body).execute()
            doc_id = doc.get('documentId')
            console.print(f"[green]Document Created! ID: {doc_id}[/green]")
            
            # Generate Smart Content
            self._insert_starter_content(doc_id, title)
            
            return doc_id
        except Exception as e:
            console.print(f"[bold red]Error creating document: {e}[/bold red]")
            return None

    def _insert_starter_content(self, doc_id, document_name):
        """Generates and inserts structured content based on the document name."""
        keywords = ["project", "plan", "proposal", "report", "strategy"]
        is_professional = any(k in document_name.lower() for k in keywords)

        if is_professional:
            content_blocks = [
                {"text": f"{document_name}\n", "is_title": True},
                {"text": "\nExecutive Summary\n", "is_header": True},
                {"text": "Provide a brief overview of the purpose of this document.\n", "is_body": True},
                {"text": "\nObjectives\n", "is_header": True},
                {"text": "- Define clear project goals\n- Outline expected outcomes\n", "is_body": True},
                {"text": "\nScope\n", "is_header": True},
                {"text": "Describe what is included and excluded in this project.\n", "is_body": True},
                {"text": "\nTimeline\n", "is_header": True},
                {"text": "Provide a high-level milestone plan.\n", "is_body": True},
                {"text": "\nResources\n", "is_header": True},
                {"text": "List required tools, people, and budget considerations.\n", "is_body": True},
                {"text": "\nConclusion\n", "is_header": True},
                {"text": "Summarize the overall vision and next steps.\n", "is_body": True},
            ]
        else:
            content_blocks = [
                {"text": f"{document_name}\n", "is_title": True},
                {"text": "\nOverview\n", "is_header": True},
                {"text": "General notes and information for this document.\n", "is_body": True}
            ]

        requests = []
        current_index = 1
        
        # We need to insert text in reverse order or keep track of indices.
        # Simplest is to build the full string and then apply formatting.
        full_text = ""
        for block in content_blocks:
            full_text += block["text"]

        # 1. Insert all text
        requests.append({
            'insertText': {
                'location': {'index': current_index},
                'text': full_text
            }
        })

        # 2. Apply formatting
        temp_index = 1
        for block in content_blocks:
            text_len = len(block["text"])
            if block.get("is_title"):
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': temp_index, 'endIndex': temp_index + text_len},
                        'textStyle': {'bold': True, 'fontSize': {'magnitude': 18, 'unit': 'PT'}},
                        'fields': 'bold,fontSize'
                    }
                })
            elif block.get("is_header"):
                requests.append({
                    'updateTextStyle': {
                        'range': {'startIndex': temp_index, 'endIndex': temp_index + text_len},
                        'textStyle': {'bold': True, 'fontSize': {'magnitude': 14, 'unit': 'PT'}},
                        'fields': 'bold,fontSize'
                    }
                })
            temp_index += text_len

        try:
            self.service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
            console.print(f"[green]Smart content initialized in Document {doc_id}[/green]")
        except Exception as e:
            console.print(f"[yellow]Failed to populate document content: {e}[/yellow]")

    def get_document(self, document_id):
        """Fetches a Google Doc content title."""
        try:
            console.print(f"[cyan]Fetching Doc {document_id}...[/cyan]")
            document = self.service.documents().get(documentId=document_id).execute()
            title = document.get('title')
            console.print(f"[green]Found Document: {title}[/green]")
            return {"Title": title, "ID": document_id}
        except Exception as e:
            console.print(f"[bold red]Error fetching document: {e}[/bold red]")
            return None

    def write_text(self, doc_id, content):
        """Writes text to the end of a document."""
        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': content + "\n"
                    }
                }
            ]
            self.service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
            console.print(f"[green]Text written to Document {doc_id}[/green]")
            return True
        except Exception as e:
            console.print(f"[bold red]Error writing to document: {e}[/bold red]")
            return False
