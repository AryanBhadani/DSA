"""
Secure configuration management for LeetCode credentials.
Uses environment variables to avoid hardcoding secrets.
"""

import os
import sys
from pathlib import Path

def get_leetcode_session():
    """Get LEETCODE_SESSION from environment variables."""
    session = os.environ.get("LEETCODE_SESSION")
    if not session:
        print("ERROR: LEETCODE_SESSION environment variable not set.", file=sys.stderr)
        print("Please set it using: $env:LEETCODE_SESSION='your_value'", file=sys.stderr)
        return None
    return session

def get_leetcode_csrf_token():
    """Get LEETCODE_CSRF_TOKEN from environment variables."""
    token = os.environ.get("LEETCODE_CSRF_TOKEN")
    if not token:
        print("ERROR: LEETCODE_CSRF_TOKEN environment variable not set.", file=sys.stderr)
        print("Please set it using: $env:LEETCODE_CSRF_TOKEN='your_value'", file=sys.stderr)
        return None
    return token

def validate_credentials():
    """Validate that both credentials are present."""
    session = get_leetcode_session()
    token = get_leetcode_csrf_token()
    
    if not session or not token:
        return False
    
    # Basic validation - check they're not empty
    if len(session) < 10 or len(token) < 10:
        print("ERROR: Credentials appear invalid (too short).", file=sys.stderr)
        return False
    
    return True

def print_setup_instructions():
    """Print instructions for setting up credentials securely."""
    print("""
=== LeetCode Credential Setup Instructions ===

Step 1: Get your LeetCode session cookies
-----------------------------------------
1. Open https://leetcode.com in your browser and log in
2. Press F12 to open Developer Tools
3. Go to the "Application" tab (Chrome) or "Storage" tab (Firefox)
4. Expand "Cookies" on the left sidebar
5. Click on "https://leetcode.com"
6. Find and copy the value of "LEETCODE_SESSION"
7. Find and copy the value of "csrftoken"

Step 2: Set environment variables in PowerShell
----------------------------------------------
Run these commands in PowerShell (replace YOUR_VALUES with actual values):

$env:LEETCODE_SESSION='your_session_value_here'
$env:LEETCODE_CSRF_TOKEN='your_csrf_token_value_here'

To make these persistent across PowerShell sessions, use:

[System.Environment]::SetEnvironmentVariable('LEETCODE_SESSION', 'your_value', 'User')
[System.Environment]::SetEnvironmentVariable('LEETCODE_CSRF_TOKEN', 'your_value', 'User')

Step 3: Verify setup
--------------------
Run this command to verify:
python -c "import os; print('Session:', 'LEETCODE_SESSION' in os.environ); print('Token:', 'LEETCODE_CSRF_TOKEN' in os.environ)"

Security Notes:
--------------
- Never paste credentials into chat or commit them to Git
- These values are session cookies that expire periodically
- Refresh them if authentication fails
- The old project's credentials are not used or exposed
""")
