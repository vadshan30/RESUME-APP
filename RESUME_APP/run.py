#!/usr/bin/env python
"""
Main entry point for the Career Assistant application.
Run this file to start the server.

Requirements:
- Python 3.12
- Virtual environment with dependencies installed
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Verify Python version
if sys.version_info < (3, 12) or sys.version_info >= (3, 13):
    print("=" * 60)
    print("WARNING: This application requires Python 3.12")
    print(f"Current Python version: {sys.version}")
    print("=" * 60)
    print("\nPlease install Python 3.12 and create a new virtual environment:")
    print("  python3.12 -m venv venv")
    print("  # Windows: venv\\Scripts\\activate")
    print("  # Linux/Mac: source venv/bin/activate")
    print("  pip install -r backend/requirements.txt\n")
    sys.exit(1)

try:
    from backend.app import create_app
except ImportError as e:
    print("=" * 60)
    print("ERROR: Failed to import Flask application")
    print(f"Error: {e}")
    print("=" * 60)
    print("\nPlease ensure:")
    print("1. Virtual environment is activated")
    print("2. Dependencies are installed: pip install -r backend/requirements.txt")
    print("3. You're running from the project root directory\n")
    sys.exit(1)

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Career Assistant Web Application")
    print("=" * 60)
    print(f"Python version: {sys.version.split()[0]}")
    print(f"Project root: {project_root}")
    
    try:
        app = create_app()
        port = int(os.getenv('PORT', 5000))
        
        print(f"\n✅ Application initialized successfully")
        print(f"📡 Starting server on http://localhost:{port}")
        print(f"🌐 Open your browser and navigate to: http://localhost:{port}")
        print("\n" + "=" * 60)
        print("Press CTRL+C to stop the server")
        print("=" * 60 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=port)
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR: Failed to start application")
        print(f"Error: {e}")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Check that all dependencies are installed")
        print("2. Verify Python version is 3.12")
        print("3. Ensure virtual environment is activated")
        print("4. Check that backend/uploads directory exists\n")
        sys.exit(1)

