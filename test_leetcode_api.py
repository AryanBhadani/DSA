"""
Test LeetCode API access without authentication.
Attempts to retrieve public profile data and solved problems.
"""

import requests
import json
import urllib3

# Suppress SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GRAPHQL_URL = "https://leetcode.com/graphql/"

def test_user_profile_query():
    """Test querying user profile data without authentication."""
    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
        }
    }
    """
    
    payload = {
        "query": query,
        "variables": {"username": "Aryanbhadani123"},
        "operationName": "getUserProfile"
    }
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"\nResponse Body:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_recent_submissions_query():
    """Test querying recent submissions without authentication."""
    query = """
    query recentSubmissions($username: String!) {
        recentSubmissionList(username: $username) {
            title
            titleSlug
            statusDisplay
            lang
            timestamp
        }
    }
    """
    
    payload = {
        "query": query,
        "variables": {"username": "Aryanbhadani123"},
        "operationName": "recentSubmissions"
    }
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        print(f"\nRecent Submissions - Status Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Testing LeetCode API Access Without Authentication")
    print("=" * 60)
    
    print("\n--- Test 1: User Profile Query ---")
    profile_result = test_user_profile_query()
    
    print("\n--- Test 2: Recent Submissions Query ---")
    submissions_result = test_recent_submissions_query()
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

