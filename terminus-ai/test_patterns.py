import re

patterns = [
    (r'^(check|list).*(mail|email|messages)$', 'Pattern 1'),
    (r'(check|list)\s+(last|recent)?\s*(mail|email|messages)', 'Pattern 2'),
]

tests = ['check mail', 'list mail', 'check last mail', 'list recent mail']

for test_str in tests:
    for pattern, name in patterns:
        match = re.search(pattern, test_str.lower())
        if match:
            print(f'✓ {name} matches "{test_str}"')
            break
    else:
        print(f'✗ No pattern matches "{test_str}"')
