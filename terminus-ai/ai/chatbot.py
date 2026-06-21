import json
import os
from rich.console import Console

console = Console()


class ChatbotEngine:
    """
    Conversational AI engine for TERMINUS AI.
    
    Uses OpenAI to understand ANY natural language input and either:
    1. Returns a structured action for Google Workspace execution
    2. Returns a conversational response for questions/explanations
    
    Maintains conversation history for multi-turn context.
    """

    SYSTEM_PROMPT = """You are TERMINUS AI, a Google Workspace assistant.
Return ONLY valid JSON in one of two modes:

MODE 1 "action" - for Google API operations:
{"mode":"action","intent":{"service":"<svc>","action":"<act>","argument":null,"confidence":1.0}}

Services: calendar(list|create|plan), gmail(list), drive(list|upload|create-folder), sheets(create), docs(create|get), forms(create|get), smart(smart_doc|smart_sheet|smart_email|build_workflow|smart_workday), briefing(daily_briefing|prepare_meeting|organize_emails|send_digest), workflow(project_setup|meeting_summary|workday_automation), scheduler(email_digest)

MODE 2 "chat" - for questions, greetings, help:
{"mode":"chat","response":"<brief_answer>"}

Examples: "show meetings"→action calendar.list, "create sheet Budget"→action sheets.create arg Budget, "hello"→chat, "what can you do"→chat.
Keep chat responses short. Return ONLY JSON.
"""

    def __init__(self):
        self.config = self._load_config()
        self.client = None
        self.provider = self.config.get("provider", "openai")
        self.model = "gpt-4o-mini"
        self.available = False
        self.conversation_history = []

        self._initialize()

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

    def _initialize(self):
        """Initialize the AI client (OpenAI or Gemini)."""
        self.provider = self.config.get("provider", "openai")

        if self.provider == "gemini":
            api_key = self.config.get("gemini_api_key")
            if not api_key:
                console.print("[yellow]⚠ No Gemini API key found in config.json.[/yellow]")
                return
            
            try:
                from google import genai
                self.client = genai.Client(api_key=api_key)
                # The model name in the new SDK might just be "gemini-1.5-flash" or similar
                model_name = self.config.get("gemini_model", "gemini-2.0-flash") 
                self.model = model_name
                self.available = True
                console.print(f"[green][AI] TERMINUS AI Ready (Provider: Google Gemini | Model: {model_name})[/green]")
            except ImportError as e:
                 console.print(f"[yellow]⚠ google-genai package not installed or import failed: {e}. Run: pip install google-genai[/yellow]")
            except Exception as e:
                 console.print(f"[red]Gemini initialization error: {e}[/red]")
            return

        # Fallback to OpenAI/Ollama
        api_key = os.environ.get("OPENAI_API_KEY") or self.config.get("openai_api_key", "")
        if not api_key:
             console.print("[yellow]⚠ No OpenAI API key found. Set OPENAI_API_KEY env var or add to config.json.[/yellow]")
             return

        try:
            import openai
            base_url = self.config.get("openai_base_url")
            if base_url:
                self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
                console.print(f"[green]🤖 TERMINUS AI Chatbot ready! (Base URL: {base_url})[/green]")
            else:
                self.client = openai.OpenAI(api_key=api_key)
                console.print("[green]🤖 TERMINUS AI Chatbot ready![/green]")

            self.model = self.config.get("openai_model", "gpt-4o-mini")
            self.available = True
        except ImportError:
            console.print("[yellow]⚠ OpenAI package not installed. Run: pip install openai[/yellow]")
        except Exception as e:
            console.print(f"[yellow]⚠ OpenAI initialization failed: {e}[/yellow]")

    def chat(self, user_input):
        """
        Process user input through the chatbot engine.
        """
        if not self.available:
            return {
                "mode": "chat",
                "response": "⚠️ AI provider is not configured. Please check your config.json."
            }

        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Keep conversation history small to save context window
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

        try:
            result_text = ""
            
            if self.provider == "gemini":
                # Construct prompt for Gemini (stateless approach for simplicity)
                full_prompt = f"{self.SYSTEM_PROMPT}\n\nConversation History:\n"
                for msg in self.conversation_history:
                    role_str = "User" if msg["role"] == "user" else "Assistant"
                    full_prompt += f"{role_str}: {msg['content']}\n"
                full_prompt += "\nAssistant (JSON):"
                
                try:
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=full_prompt
                    )
                    result_text = response.text.strip()
                except Exception as e:
                    # Basic error handling for potential quota issues or API errors
                    console.print(f"[red]Gemini API Error: {e}[/red]")
                    if "429" in str(e) or "quota" in str(e).lower():
                        return {
                            "mode": "fallback",
                            "response": "Gemini quota exceeded."
                        }
                    raise e
                
                # Cleanup markdown code blocks if Gemini adds them
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.startswith("```"):
                    result_text = result_text[3:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                result_text = result_text.strip()

            else:
                # OpenAI / Ollama Logic
                messages = [
                    {"role": "system", "content": self.SYSTEM_PROMPT}
                ] + self.conversation_history

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,
                    max_tokens=150
                )
                result_text = response.choices[0].message.content.strip()

            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": result_text if self.provider == "openai" else result_text # For Gemini we might want to store the raw text
            })

            # Parse JSON response
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Retry parsing (sometimes minor format issues) or fallback to chat
                return {
                    "mode": "chat",
                    "response": result_text
                }

            if result.get("mode") == "action" and "intent" in result:
                return result
            elif result.get("mode") == "chat" and "response" in result:
                return result
            else:
                return {
                    "mode": "chat",
                    "response": result_text
                }

        except Exception as e:
            error_str = str(e)
            console.print(f"[dim red]Chatbot error: {e}[/dim red]")
            return {
                "mode": "error",
                "response": f"Sorry, I encountered an error: {error_str}"
            }

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
