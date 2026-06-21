"""
Alternative entry point for the Career Assistant application.
For best results, use run.py from the project root instead.
"""
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from backend.app import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f"\n✅ Career Assistant starting on http://localhost:{port}\n")
    app.run(debug=True, host='0.0.0.0', port=port)

