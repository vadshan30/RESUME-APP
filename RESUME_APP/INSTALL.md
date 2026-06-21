# Installation Guide - Python 3.12

## Step-by-Step Installation

### Step 1: Install Python 3.12

**Windows:**
1. Download Python 3.12 from [python.org/downloads](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. ✅ Check "Install for all users" (optional)

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

**Mac (using Homebrew):**
```bash
brew install python@3.12
```

**Verify installation:**
```bash
python3.12 --version
# Should show: Python 3.12.x
```

### Step 2: Clone/Navigate to Project

```bash
cd resumeapp
# or
git clone <your-repo-url>
cd resumeapp
```

### Step 3: Create Virtual Environment

```bash
# Using Python 3.12 specifically
python3.12 -m venv venv

# Or if python3.12 is your default python:
python -m venv venv
```

### Step 4: Activate Virtual Environment

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Verify activation:**
You should see `(venv)` at the start of your terminal prompt.

### Step 5: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 6: Install Dependencies

```bash
pip install -r backend/requirements.txt
```

This will install:
- Flask 3.0.0
- Flask-CORS
- pdfplumber
- PyPDF2
- spaCy (optional)
- And other dependencies

### Step 7: Verify Installation

```bash
python -c "import flask; print(f'Flask {flask.__version__} installed successfully')"
```

Should output: `Flask 3.0.0 installed successfully`

### Step 8: Run Application

```bash
python run.py
```

You should see:
```
============================================================
🚀 Career Assistant Web Application
============================================================
Python version: 3.12.x
✅ Application initialized successfully
📡 Starting server on http://localhost:5000
```

### Step 9: Open Browser

Navigate to: `http://localhost:5000`

## Troubleshooting

### "python3.12: command not found"

**Solution:** Python 3.12 is not in your PATH or not installed.
- Windows: Reinstall Python 3.12 with "Add to PATH" checked
- Linux: Use `sudo apt install python3.12` or build from source
- Mac: Use `brew install python@3.12` or download from python.org

### "ModuleNotFoundError: No module named 'flask'"

**Solution:**
1. Ensure virtual environment is activated (`(venv)` in prompt)
2. Reinstall: `pip install -r backend/requirements.txt`
3. Verify: `pip list | grep Flask`

### "This application requires Python 3.12"

**Solution:** You're using Python 3.11 or 3.13. Create a new venv with Python 3.12:
```bash
python3.12 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
```

### Virtual environment not activating

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

## Next Steps

After successful installation:
1. See [SETUP.md](./SETUP.md) for configuration
2. See [QUICKSTART.md](./QUICKSTART.md) for quick usage guide
3. See [README.md](./README.md) for full documentation

