"""
Test authenticated LeetCode API retrieval.
Requires LEETCODE_SESSION and LEETCODE_CSRF_TOKEN environment variables.
"""

import requests
import json
import sys
import urllib3
from config import validate_credentials, get_leetcode_session, get_leetcode_csrf_token

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GRAPHQL_URL = "https://leetcode.com/graphql/"

def test_authenticated_submission_list():
    """Test retrieving complete submission list with authentication."""
    if not validate_credentials():
        print("Skipping test: credentials not configured", file=sys.stderr)
        return None
    
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
        "Origin": "https://leetcode.com",
        "User-Agent": "Mozilla/5.0 (compatible; leetcode-sync-fresh/1.0)",
        "x-csrftoken": get_leetcode_csrf_token(),
    })
    session.cookies.set("LEETCODE_SESSION", get_leetcode_session(), domain="leetcode.com")
    session.cookies.set("csrftoken", get_leetcode_csrf_token(), domain="leetcode.com")
    
    query = """
    query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String) {
        submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug) {
            lastKey
            hasNext
            submissions {
                id
                statusDisplay
                lang
                timestamp
                title
                titleSlug
            }
        }
    }
    """
    
    payload = {
        "query": query,
        "variables": {
            "offset": 0,
            "limit": 20,
            "lastKey": None,
            "questionSlug": None
        },
        "operationName": "submissionList"
    }
    
    try:
        resp = session.post(GRAPHQL_URL, json=payload)
        print(f"Authenticated Submission List - Status: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"HTTP Error: {resp.status_code}", file=sys.stderr)
            return None
        
        data = resp.json()
        
        if data.get("errors"):
            print(f"GraphQL Errors: {data['errors']}", file=sys.stderr)
            return None
        
        print(f"Response preview:")
        print(json.dumps(data, indent=2)[:1000])
        
        submission_list = data.get("data", {}).get("submissionList")
        if submission_list is None:
            print("ERROR: submissionList is null - authentication may have failed", file=sys.stderr)
            return None
        
        submissions = submission_list.get("submissions")
        if submissions is None:
            print("ERROR: submissions field is null", file=sys.stderr)
            return None
        
        print(f"\nSubmissions retrieved: {len(submissions)}")
        print(f"hasNext: {submission_list.get('hasNext')}")
        
        if len(submissions) == 0:
            print("WARNING: No submissions retrieved", file=sys.stderr)
        
        return data
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

def test_submission_details(submission_id):
    """Test retrieving submission details (including source code)."""
    if not validate_credentials():
        print("Skipping test: credentials not configured", file=sys.stderr)
        return None
    
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
        "Origin": "https://leetcode.com",
        "User-Agent": "Mozilla/5.0 (compatible; leetcode-sync-fresh/1.0)",
        "x-csrftoken": get_leetcode_csrf_token(),
    })
    session.cookies.set("LEETCODE_SESSION", get_leetcode_session(), domain="leetcode.com")
    session.cookies.set("csrftoken", get_leetcode_csrf_token(), domain="leetcode.com")
    
    query = """
    query submissionDetails($submissionId: Int!) {
        submissionDetails(submissionId: $submissionId) {
            code
            runtime
            memory
            timestamp
            lang {
                name
            }
            question {
                questionId
                title
                titleSlug
                difficulty
                topicTags {
                    name
                }
            }
        }
    }
    """
    
    payload = {
        "query": query,
        "variables": {"submissionId": int(submission_id)},
        "operationName": "submissionDetails"
    }
    
    try:
        resp = session.post(GRAPHQL_URL, json=payload)
        print(f"\nSubmission Details - Status: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"HTTP Error: {resp.status_code}", file=sys.stderr)
            return None
        
        data = resp.json()
        
        if data.get("errors"):
            print(f"GraphQL Errors: {data['errors']}", file=sys.stderr)
            return None
        
        details = data.get("data", {}).get("submissionDetails")
        if details is None:
            print("ERROR: submissionDetails is null", file=sys.stderr)
            return None
        
        code = details.get("code")
        if code:
            print(f"Source code length: {len(code)} characters")
            print(f"Language: {details.get('lang', {}).get('name')}")
            print(f"Problem: {details.get('question', {}).get('title')}")
            print(f"Code preview (first 200 chars):")
            print(code[:200])
        else:
            print("WARNING: No source code in response", file=sys.stderr)
        
        return data
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Authenticated LeetCode API Retrieval")
    print("=" * 60)
    
    print("\n--- Step 1: Test Submission List ---")
    submission_result = test_authenticated_submission_list()
    
    if submission_result:
        # Get first submission ID for testing details
        submissions = submission_result.get("data", {}).get("submissionList", {}).get("submissions", [])
        if submissions:
            first_id = submissions[0].get("id")
            print(f"\n--- Step 2: Test Submission Details (ID: {first_id}) ---")
            details_result = test_submission_details(first_id)
        else:
            print("\nNo submissions available to test details", file=sys.stderr)
    else:
        print("\nSkipping submission details test - no submission list retrieved", file=sys.stderr)
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

