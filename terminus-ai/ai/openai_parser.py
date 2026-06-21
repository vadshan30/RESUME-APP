import json
import os
from rich.console import Console

console = Console()

class OpenAIParser:
    """
    Advanced parser using OpenAI API for natural language understanding.
    Falls back to regex-based parsing if OpenAI is not configured.
    """
    def __init__(self):
        self.config = self._load_config()
        self.use_openai = self.config.get("use_openai", False)
        self.openai_available = False
        
        if self.use_openai:
            try:
                import openai
                # Priority: env var > config.json
                api_key = os.environ.get("OPENAI_API_KEY") or self.config.get("openai_api_key", "")
                if api_key:
                    self.client = openai.OpenAI(api_key=api_key)
                    self.model = self.config.get("openai_model", "gpt-3.5-turbo")
                    self.openai_available = True
                    console.print("[green]🤖 OpenAI API enabled![/green]")
                else:
                    console.print("[yellow]⚠ OpenAI API key not configured. Set OPENAI_API_KEY env var or add to config.json.[/yellow]")
            except ImportError:
                console.print("[yellow]⚠ OpenAI package not installed. Run: pip install openai[/yellow]")
            except Exception as e:
                console.print(f"[yellow]⚠ OpenAI initialization failed: {e}[/yellow]")
    
    def _load_config(self):
        """Load configuration from config.json"""
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"use_openai": False}
        except Exception as e:
            console.print(f"[yellow]Config load error: {e}[/yellow]")
            return {"use_openai": False}
    
    def parse(self, user_input):
        """
        Parse user input using OpenAI API.
        Returns structured intent: {service, action, argument, confidence}
        """
        if not self.openai_available:
            return None  # Will fall back to regex parser
        
        try:
            # Create a prompt for OpenAI to extract intent
            system_prompt = """You are an intent classifier for TERMINUS AI, a Google Workspace automation assistant.

Your job is to analyze user commands and return a JSON object with:
- service: one of [calendar, drive, gmail, docs, sheets, forms, smart, briefing, workflow, scheduler, general]
- action: the specific action (list, create, upload, plan, smart_doc, smart_sheet, etc.)
- argument: any additional parameters (can be null)
- confidence: 0.0 to 1.0

Examples:
"tomorrow meeting" → {"service": "calendar", "action": "list", "argument": null, "confidence": 1.0}
"create sheet Budget" → {"service": "sheets", "action": "create", "argument": "Budget", "confidence": 1.0}
"plan my day" → {"service": "calendar", "action": "plan", "argument": null, "confidence": 1.0}
"create smart doc Project" → {"service": "smart", "action": "smart_doc", "argument": "Project", "confidence": 1.0}
"daily briefing" → {"service": "briefing", "action": "daily_briefing", "argument": null, "confidence": 1.0}

Return ONLY valid JSON, no explanation."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            result = json.loads(result_text)
            
            # Validate result
            if all(k in result for k in ["service", "action", "confidence"]):
                console.print(f"[dim cyan]🤖 OpenAI: {result['service']}.{result['action']}[/dim cyan]")
                return result
            else:
                console.print("[yellow]⚠ Invalid OpenAI response format[/yellow]")
                return None
                
        except json.JSONDecodeError:
            console.print(f"[yellow]⚠ OpenAI returned invalid JSON: {result_text}[/yellow]")
            return None
        except Exception as e:
            console.print(f"[yellow]⚠ OpenAI API error: {e}[/yellow]")
            return None
