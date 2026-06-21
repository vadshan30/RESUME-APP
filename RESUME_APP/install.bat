@echo off
echo Installing Python 3.12...
curl -o python-installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
echo Python installed. Setting up project...
timeout /t 5
python -m venv venv
call venv\Scripts\activate.bat
pip install -r backend\requirements.txt
echo Starting server...
python run.py