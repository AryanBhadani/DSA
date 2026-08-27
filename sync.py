"""
sync.py

Pulls your Accepted LeetCode submissions and writes each solved problem into
this repo as:

    problems/<questionId>-<title-slug>/
        README.md        (title, difficulty, tags, link to problem)
        solution.<ext>    (your submitted code)

It keeps a record of already-synced submission ids in `synced_submissions.json`
so re-runs only add NEW solves, and won't spam duplicate commits.

Auth:
    LeetCode does not expose your own solution code through a public API.
    You must supply your logged-in session cookies as environment variables
    (set as GitHub Secrets in the Action — see .github/workflows/leetcode-sync.yml
    and SETUP.md for how to get them):

        LEETCODE_SESSION
        LEETCODE_CSRF_TOKEN

Notes:
    - This uses LeetCode's internal GraphQL endpoint. It is not an official/
      documented public API, so it can break if LeetCode changes their schema.
    - Only Accepted submissions are synced. If you solve the same problem in
      multiple languages, each language gets its own subfolder.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

import requests

GRAPHQL_URL = "https://leetcode.com/graphql/"
REPO_ROOT = Path(__file__).resolve().parent
PROBLEMS_DIR = REPO_ROOT / "problems"
SYNCED_FILE = REPO_ROOT / "synced_submissions.json"

LANG_EXTENSIONS = {
    "python": "py",
    "python3": "py",
    "c": "c",
    "cpp": "cpp",
    "csharp": "cs",
    "java": "java",
    "javascript": "js",
    "typescript": "ts",
    "kotlin": "kt",
    "swift": "swift",
    "golang": "go",
    "ruby": "rb",
    "scala": "scala",
    "rust": "rs",
    "php": "php",
    "erlang": "erl",
    "elixir": "ex",
    "racket": "rkt",
    "dart": "dart",
    "mysql": "sql",
    "mssql": "sql",
    "oraclesql": "sql",
}

SUBMISSION_LIST_QUERY = """
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

SUBMISSION_DETAILS_QUERY = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    code
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


def get_session():
    leetcode_session = os.environ.get("LEETCODE_SESSION")
    csrf_token = os.environ.get("LEETCODE_CSRF_TOKEN")

    if not leetcode_session or not csrf_token:
        print(
            "ERROR: LEETCODE_SESSION and LEETCODE_CSRF_TOKEN env vars are required.",
            file=sys.stderr,
        )
        sys.exit(1)

    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "Origin": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (compatible; leetcode-dsa-sync/1.0)",
            "x-csrftoken": csrf_token,
        }
    )
    session.cookies.set("LEETCODE_SESSION", leetcode_session, domain="leetcode.com")
    session.cookies.set("csrftoken", csrf_token, domain="leetcode.com")
    return session


def load_synced():
    if SYNCED_FILE.exists():
        return json.loads(SYNCED_FILE.read_text())
    return {}


def save_synced(synced):
    SYNCED_FILE.write_text(json.dumps(synced, indent=2, sort_keys=True))


def fetch_accepted_submissions(session, max_pages=20, page_size=20):
    """Yield accepted submissions, newest first, until we've paged through
    everything LeetCode will give us (it caps history depth)."""
    offset = 0
    last_key = None
    for _ in range(max_pages):
        payload = {
            "query": SUBMISSION_LIST_QUERY,
            "variables": {
                "offset": offset,
                "limit": page_size,
                "lastKey": last_key,
                "questionSlug": "",
            },
            "operationName": "submissionList",
        }
        resp = session.post(GRAPHQL_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()

        if data.get("errors"):
            print(f"GraphQL error: {data['errors']}", file=sys.stderr)
            break

        result = data["data"]["submissionList"]
        for sub in result["submissions"]:
            if sub["statusDisplay"] == "Accepted":
                yield sub

        if not result["hasNext"]:
            break

        last_key = result["lastKey"]
        offset += page_size
        time.sleep(0.5)  # be polite to the API


def fetch_submission_details(session, submission_id):
    payload = {
        "query": SUBMISSION_DETAILS_QUERY,
        "variables": {"submissionId": int(submission_id)},
        "operationName": "submissionDetails",
    }
    resp = session.post(GRAPHQL_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("errors"):
        print(f"GraphQL error fetching details for {submission_id}: {data['errors']}", file=sys.stderr)
        return None
    return data["data"]["submissionDetails"]


def slugify_folder(question_id, title_slug):
    return f"{question_id}-{title_slug}"


def write_problem(details, submission):
    question = details["question"]
    lang_name = details["lang"]["name"].lower()
    ext = LANG_EXTENSIONS.get(lang_name, "txt")

    folder_name = slugify_folder(question["questionId"], question["titleSlug"])
    folder = PROBLEMS_DIR / folder_name
    folder.mkdir(parents=True, exist_ok=True)

    solution_path = folder / f"solution.{ext}"
    solution_path.write_text(details["code"])

    tags = ", ".join(t["name"] for t in question.get("topicTags", []))
    readme_path = folder / "README.md"
    readme_path.write_text(
        f"# {question['questionId']}. {question['title']}\n\n"
        f"**Difficulty:** {question['difficulty']}\n\n"
        f"**Tags:** {tags}\n\n"
        f"**Link:** https://leetcode.com/problems/{question['titleSlug']}/\n\n"
        f"**Language:** {details['lang']['name']}\n\n"
        f"Solved on: {time.strftime('%Y-%m-%d', time.localtime(int(submission['timestamp'])))}\n"
    )
    return folder_name


def main():
    PROBLEMS_DIR.mkdir(exist_ok=True)
    session = get_session()
    synced = load_synced()

    new_count = 0
    for submission in fetch_accepted_submissions(session):
        sub_id = str(submission["id"])
        key = f"{submission['titleSlug']}:{submission['lang']}"

        # Skip if we've already synced an accepted solution for this
        # problem+language combo (keeps the repo to one solution per language).
        if key in synced:
            continue

        details = fetch_submission_details(session, sub_id)
        if not details:
            continue

        folder_name = write_problem(details, submission)
        synced[key] = {"submission_id": sub_id, "folder": folder_name}
        new_count += 1
        print(f"Synced: {folder_name} ({submission['lang']})")
        time.sleep(0.5)

    save_synced(synced)
    print(f"\nDone. {new_count} new solution(s) synced.")


if __name__ == "__main__":
    main()
