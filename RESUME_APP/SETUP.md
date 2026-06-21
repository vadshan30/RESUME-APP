# Setup Instructions

## Prerequisites

- **Python 3.12** (required - not 3.11 or 3.13)
- pip (Python package manager)
- Virtual environment support

## Quick Start

### 1. Verify Python Version

```bash
python --version
# Should show: Python 3.12.x
```

If you don't have Python 3.12:
- **Windows:** Download from [python.org](https://www.python.org/downloads/)
- **Linux:** `sudo apt install python3.12 python3.12-venv` (or use pyenv)
- **Mac:** `brew install python@3.12` (or use pyenv)

### 2. Create Virtual Environment

```bash
# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Or if python3.12 is your default:
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies

```bash
# From project root directory
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 2. Download spaCy Language Model (Optional but Recommended)

```bash
python -m spacy download en_core_web_sm
```

Note: If you skip this step, the app will still work but with basic NLP capabilities.

### 3. Set Environment Variables

Create a `.env` file in the root directory:

```env
PORT=5000
UPLOAD_FOLDER=./backend/uploads
MAX_FILE_SIZE=10485760
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 5. Run the Application

**Recommended method (from project root):**
```bash
python run.py
```

**Alternative method:**
```bash
python backend/app.py
```

The application will start and display:
- ✅ Application initialized successfully
- 📡 Server URL: http://localhost:5000
- 🌐 Browser link

The application will be available at `http://localhost:5000`

### 6. Open in Browser

Navigate to `http://localhost:5000` in your web browser.

## Troubleshooting

### Issue: Python version error

**Error:** "This application requires Python 3.12"

**Solution:** 
- Install Python 3.12
- Create a new virtual environment: `python3.12 -m venv venv`
- Activate it and reinstall dependencies

### Issue: ModuleNotFoundError: No module named 'flask'

**Solution:** 
1. Ensure virtual environment is activated (you should see `(venv)` in prompt)
2. Verify installation: `pip list | grep Flask`
3. Reinstall: `pip install -r backend/requirements.txt`
4. If using Python 3.13, downgrade to Python 3.12

### Issue: Port already in use

**Solution:** Change the port in `backend/app.py` or set `PORT` environment variable.

### Issue: PDF extraction not working

**Solution:** Make sure `pdfplumber` and `PyPDF2` are installed. Try both libraries as fallback.

### Issue: CORS errors

**Solution:** The Flask-CORS is already configured. If issues persist, check that the frontend is being served from the same origin or update CORS settings in `backend/app/__init__.py`.

## Development Mode

The application runs in debug mode by default when using `python run.py`.

For Windows PowerShell:
```powershell
$env:FLASK_ENV="development"
$env:FLASK_DEBUG="1"
python run.py
```

For Linux/Mac:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

## Production Deployment

See the main README.md for deployment instructions to Heroku, Railway, or other platforms.

