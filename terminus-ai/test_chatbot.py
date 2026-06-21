#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from ai.parser import AIParser

parser = AIParser()

test_commands = [
    "what is my today plan",
    "when is my next meeting",
    "explain tomorrow meeting",
    "summarize my emails",
    "do i have any meetings today",
    "what files did i upload",
    "hello",
    "help",
    "check mail",
]

print("\nTesting natural language patterns:\n")
for cmd in test_commands:
    result = parser.parse(cmd)
    print(f"  '{cmd}'")
    print(f"    -> {result['service']}.{result['action']} (confidence: {result['confidence']})\n")
