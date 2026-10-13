"""
Test retrieving complete solved problem list from LeetCode.
Attempts to get all accepted submissions, not just recent ones.
"""

import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

GRAPHQL_URL = "https://leetcode.com/graphql/"

def test_accepted_submissions_query():
    """Test querying for complete submission list (requires auth)."""
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
        response = requests.post(GRAPHQL_URL, json=payload)
        print(f"Submission List - Status Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_user_solved_query():
    """Test querying for user's solved problems list."""
    query = """
    query userSolved($username: String!) {
        matchedUser(username: $username) {
            submitStats: submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                }
            }
            accepteds {
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
        "variables": {"username": "Aryanbhadani123"},
        "operationName": "userSolved"
    }
    
    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        print(f"\nUser Solved - Status Code: {response.status_code}")
        print(f"Response Body:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Complete Solved Problem Retrieval")
    print("=" * 60)
    
    print("\n--- Test 1: Submission List Query (No Auth) ---")
    submissions_result = test_accepted_submissions_query()
    
    print("\n--- Test 2: User Solved Query ---")
    solved_result = test_user_solved_query()
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

