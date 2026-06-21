
import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")

try:
    import google.genai
    print(f"✅ google.genai imported successfully from: {google.genai.__file__}")
except ImportError as e:
    print(f"❌ ImportError: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

try:
    import google.generativeai
    print(f"⚠ google.generativeai still importable from: {google.generativeai.__file__}")
except:
    print("✅ google.generativeai not found (expected)")
