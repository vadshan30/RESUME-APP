#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from ai.parser import AIParser

parser = AIParser()

test_commands = [
    "check mail",
    "list mail",
    "check last mail",
    "list recent mail",
    "show my meetings",
]

print("Testing mail command patterns:\n")
for cmd in test_commands:
    result = parser.parse(cmd)
    print(f"Command: '{cmd}'")
    print(f"  Service: {result['service']}")
    print(f"  Action: {result['action']}")
    print(f"  Confidence: {result['confidence']}\n")
