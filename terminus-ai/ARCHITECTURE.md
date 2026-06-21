# TERMINUS AI - Technical Architecture

## Overview
TERMINUS AI is a modular CLI application built in Python that acts as a unified interface for Google Workspace APIs. It uses a clean, layered architecture to separate concerns between the user interface, logic, and external API calls.

## Tech Stack
- **Language**: Python 3.10+
- **CLI Framework**: `typer` (for command routing)
- **UI/UX**: `rich` (for beautiful tables, panels, and spinners)
- **Authentication**: `google-auth-oauthlib` (OAuth 2.0)
- **API Client**: `google-api-python-client`

## Directory Structure & Modules

### 1. `main.py` (The Controller)
- Entry point of the application.
- Handles top-level commands (`login`, `calendar`, `drive`, `run`).
- Orchestrates the flow between the **AI Parser** and **Services**.

### 2. `auth/` (Security)
- **`auth.py`**: Manages the OAuth 2.0 flow.
- secure storage of `credentials.json` and `token.json`.
- Handles token refreshing automatically.

### 3. `ai/` (Intelligence)
- **`parser.py`**: A Rule-based NLP engine using Regex.
- Extracts **Intent** (Service + Action) and **Entities** (Arguments) from natural language.
- *Future Upgrade*: Replace Regex with local LLM (e.g., Llama 3) for context-aware parsing.

### 4. `services/` (The Engine)
- **`calendar.py`**: Interfaces with Google Calendar API.
- **`drive.py`**: Handles File and Folder operations via Google Drive API.
- **`gmail.py`**: Fetches messages via Gmail API.
- **`docs.py` / `forms.py`**: Retrieve metadata for Docs and Forms.
- *Design Pattern*: Each service is a standalone class, making it easy to mock for testing.

### 5. `utils/` (Presentation)
- **`formatter.py`**: Centralizes all UI logic.
- Ensures consistent look-and-feel (colors, borders, spinners) across the app.

## Future Roadmap
1.  **Write Capabilities for Gmail/Docs**: Send emails and edit documents from the CLI.
2.  **Local LLM Integration**: Use a small model to summarize emails or draft replies.
3.  **Voice Mode**: Add Speech-to-Text to control the CLI with voice commands.
