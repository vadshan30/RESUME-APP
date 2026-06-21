
import sys
import os

sys.path.insert(0, '.')
print(f"CWD: {os.getcwd()}")

from ai.chatbot import ChatbotEngine

print("--- Testing ChatbotEngine ---")
try:
    engine = ChatbotEngine()
    print(f"Chatbot Available: {engine.available}")
    print(f"Provider: {engine.provider}")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
