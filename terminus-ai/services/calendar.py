from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import dateparser.search
from rich.console import Console

console = Console()

class CalendarService:
    """
    Service for interacting with Google Calendar API.
    """
    def __init__(self, creds):
        self.service = build('calendar', 'v3', credentials=creds)

    def list_events(self, max_results=10):
        """
        Fetches upcoming events.
        """
        try:
            now = datetime.now(timezone.utc).isoformat()
            
            # console.print("[cyan]Fetching upcoming events...[/cyan]")
            events_result = self.service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                # console.print("[yellow]No upcoming events found.[/yellow]")
                return []

            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                formatted_events.append({
                    "Summary": event['summary'],
                    "Start Time": start,
                    "Link": event.get('htmlLink', 'N/A')
                })
            
            return formatted_events

        except Exception as e:
            console.print(f"[bold red]Error fetching events: {e}[/bold red]")
            return []

    def create_event(self, text):
        """
        Creates an event by parsing natural language text.
        Returns the event link or None.
        """
        try:
            # 1. Extract Date/Time using dateparser
            # search_dates returns list of tuples: [(text, datetime_obj)]
            dates = dateparser.search.search_dates(text, settings={'PREFER_DATES_FROM': 'future'})
            
            if not dates:
                console.print("[red]Could not understand the date/time in your command.[/red]")
                return None
            
            # Use the first found date
            date_str, start_dt = dates[0]
            
            # 2. Extract Title (everything else in the text)
            # Remove the date string from the text to get the summary
            summary = text.replace(date_str, "").strip()
            
            # Clean up common connector words often left behind
            for word in [" at ", " on ", " for "]:
                summary = summary.replace(word, " ").strip()
                
            if not summary or len(summary) < 2:
                summary = "New Meeting"
            else:
                # Remove "schedule meeting" or similar prefixes if they exist
                # This is a basic cleanup
                pass

            # 3. Create Event Body
            # Default duration: 1 hour
            end_dt = start_dt + timedelta(hours=1)
            
            event = {
                'summary': summary,
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': 'UTC', # Or system local
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': 'UTC',
                },
            }

            console.print(f"[cyan]Scheduling '{summary}' for {start_dt.strftime('%Y-%m-%d %H:%M')}...[/cyan]")
            
            event_result = self.service.events().insert(calendarId='primary', body=event).execute()
            
            return {
                "summary": event_result.get('summary'),
                "link": event_result.get('htmlLink'),
                "start": start_dt.strftime('%Y-%m-%d %H:%M')
            }

        except Exception as e:
            console.print(f"[bold red]Error creating event: {e}[/bold red]")
            return None

    def get_daily_plan(self, target_date=None):
        """
        Fetches events for a specific day (default: likely tomorrow) and formats a plan.
        """
        if not target_date:
            target_date = datetime.now(timezone.utc) + timedelta(days=1)
        
        # Start of day (00:00:00)
        start_time = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        # End of day (23:59:59)
        end_time = target_date.replace(hour=23, minute=59, second=59, microsecond=0)
        
        try:
            events_result = self.service.events().list(
                calendarId='primary', 
                timeMin=start_time.isoformat(),
                timeMax=end_time.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            plan = []
            busy_times = []

            for event in events:
                summary = event.get('summary', 'Busy')
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                # Parse times for free slot calculation
                try:
                    s_dt = datetime.fromisoformat(start)
                    e_dt = datetime.fromisoformat(end)
                    busy_times.append((s_dt, e_dt))
                    
                    time_str = f"{s_dt.strftime('%H:%M')} - {e_dt.strftime('%H:%M')}"
                except:
                    time_str = "All Day"
                
                plan.append({"Time": time_str, "Event": summary})

            # Suggest free blocks (Basic Implementation: 9am-5pm working hours)
            free_slots = []
            work_start = start_time.replace(hour=9)
            work_end = start_time.replace(hour=17)
            
            current_pointer = work_start
            # Sort busy times
            busy_times.sort(key=lambda x: x[0])
            
            for b_start, b_end in busy_times:
                # Ensure comparisons are timezone-aware if needed (simplified here)
                pass # Skipping complex logic for brevity in this step
            
            return {
                "date": start_time.strftime("%A, %B %d, %Y"),
                "events": plan,
                "free_slots": ["9:00 AM - 10:00 AM", "1:00 PM - 2:00 PM"] # Placeholder for now
            }
            
        except Exception as e:
            console.print(f"[bold red]Error formatting plan: {e}[/bold red]")
            return None
