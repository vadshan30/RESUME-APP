# Quick Start Guide

Get the Career Assistant application running in 5 minutes!

## Prerequisites

- **Python 3.12** (required)
- pip (Python package manager)

## Steps

1. **Verify Python version:**
   ```bash
   python --version
   # Must be Python 3.12.x
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create venv
   python3.12 -m venv venv
   
   # Activate (Windows PowerShell):
   venv\Scripts\Activate.ps1
   # Activate (Windows CMD):
   venv\Scripts\activate.bat
   # Activate (Linux/Mac):
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

That's it! The application is now running.

## First Use

1. Click "Get Started" or navigate to "Analyze Resume"
2. Upload a PDF or text resume
3. View extracted skills
4. Try "Job Matching" by pasting a job description
5. Explore other features like recommendations, interview prep, and analytics

## Troubleshooting

**Python version error?**
- Must use Python 3.12 (not 3.11 or 3.13)
- Create new venv: `python3.12 -m venv venv`

**ModuleNotFoundError: No module named 'flask'?**
- Activate virtual environment (check for `(venv)` in prompt)
- Reinstall: `pip install -r backend/requirements.txt`

**Port already in use?**
- Change the port in `run.py` or set `PORT` environment variable

**Import errors?**
- Make sure you're in the project root directory
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r backend/requirements.txt`

**PDF extraction not working?**
- The app uses pdfplumber with PyPDF2 as fallback
- Both should be installed automatically

For more details, see [SETUP.md](./SETUP.md)

