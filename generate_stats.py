"""
generate_stats.py

Generates a LeetCode statistics SVG card for GitHub profile README.
Fetches live data from LeetCode GraphQL API and produces a dark-themed card
with total solved, difficulty breakdown, ranking, and activity heatmap.
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

GRAPHQL_URL = "https://leetcode.com/graphql/"
REPO_ROOT = Path(__file__).resolve().parent
STATS_FILE = REPO_ROOT / "leetcode_stats.svg"
LAST_UPDATE_FILE = REPO_ROOT / "last_stats_update.txt"

LEETCODE_USERNAME = os.environ.get("LEETCODE_USERNAME", "Aryanbhadani123")

USER_STATS_QUERY = """
query getUserStats($username: String!) {
  matchedUser(username: $username) {
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
      }
    }
    profile {
      ranking
      userAvatar
      realName
    }
  }
  userStatus: currentUserStatus {
    userId
  }
}
"""

RECENT_SUBMISSIONS_QUERY = """
query recentSubmissions($username: String!, $limit: Int!) {
  recentSubmissionList(username: $username, limit: $limit) {
    title
    titleSlug
    timestamp
    statusDisplay
    lang
  }
}
"""


def get_session():
    """Create a requests session for LeetCode API."""
    leetcode_session = os.environ.get("LEETCODE_SESSION")
    csrf_token = os.environ.get("LEETCODE_CSRF_TOKEN")

    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "Origin": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (compatible; leetcode-stats-generator/1.0)",
        }
    )
    
    if leetcode_session and csrf_token:
        session.cookies.set("LEETCODE_SESSION", leetcode_session, domain="leetcode.com")
        session.cookies.set("csrftoken", csrf_token, domain="leetcode.com")
        session.headers["x-csrftoken"] = csrf_token
    
    return session


def fetch_user_stats(session):
    """Fetch user statistics from LeetCode."""
    payload = {
        "query": USER_STATS_QUERY,
        "variables": {"username": LEETCODE_USERNAME},
        "operationName": "getUserStats",
    }
    
    try:
        resp = session.post(GRAPHQL_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("errors"):
            print(f"GraphQL error: {data['errors']}", file=sys.stderr)
            return None
        
        return data["data"]
    except Exception as e:
        print(f"Error fetching user stats: {e}", file=sys.stderr)
        return None


def fetch_recent_submissions(session, limit=50):
    """Fetch recent submissions for activity heatmap."""
    payload = {
        "query": RECENT_SUBMISSIONS_QUERY,
        "variables": {"username": LEETCODE_USERNAME, "limit": limit},
        "operationName": "recentSubmissions",
    }
    
    try:
        resp = session.post(GRAPHQL_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("errors"):
            print(f"GraphQL error fetching submissions: {data['errors']}", file=sys.stderr)
            return []
        
        return data["data"].get("recentSubmissionList", [])
    except Exception as e:
        print(f"Error fetching recent submissions: {e}", file=sys.stderr)
        return []


def generate_activity_heatmap(submissions):
    """Generate 52-week activity heatmap data."""
    # Initialize 52 weeks with 0 submissions
    weeks = [0] * 52
    now = datetime.now()
    
    for sub in submissions:
        if sub.get("statusDisplay") != "Accepted":
            continue
        
        timestamp = sub.get("timestamp")
        if timestamp:
            try:
                sub_date = datetime.fromtimestamp(timestamp)
                days_ago = (now - sub_date).days
                week_index = min(days_ago // 7, 51)
                weeks[51 - week_index] += 1
            except (ValueError, TypeError):
                continue
    
    return weeks


def generate_svg(stats, activity_weeks):
    """Generate SVG statistics card."""
    # Extract stats with safe defaults
    matched_user = stats.get("matchedUser", {})
    submit_stats = matched_user.get("submitStats", {}).get("acSubmissionNum", [])
    profile = matched_user.get("profile", {})
    
    # Parse difficulty counts
    easy_count = 0
    medium_count = 0
    hard_count = 0
    total_count = 0
    
    for item in submit_stats:
        difficulty = item.get("difficulty", "").lower()
        count = item.get("count", 0)
        if difficulty == "easy":
            easy_count = count
        elif difficulty == "medium":
            medium_count = count
        elif difficulty == "hard":
            hard_count = count
    
    total_count = easy_count + medium_count + hard_count
    ranking = profile.get("ranking", "N/A")
    
    # Calculate progress percentages (assuming ~3000 total problems per difficulty)
    easy_total = 3000
    medium_total = 3000
    hard_total = 1000
    
    easy_pct = min((easy_count / easy_total) * 100, 100)
    medium_pct = min((medium_count / medium_total) * 100, 100)
    hard_pct = min((hard_count / hard_total) * 100, 100)
    
    # Generate heatmap cells
    heatmap_cells = ""
    cell_size = 10
    cell_gap = 2
    for i, count in enumerate(activity_weeks):
        x = i * (cell_size + cell_gap)
        intensity = min(count * 20, 255)
        color = f"rgb({intensity}, {int(255 - intensity * 0.5)}, {int(255 - intensity * 0.8)})" if count > 0 else "#2d333b"
        heatmap_cells += f'<rect x="{x}" y="280" width="{cell_size}" height="{cell_size}" fill="{color}" rx="2" />'
    
    # Current date
    date_str = datetime.now().strftime("%B %Y")
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="600" height="340" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 20px; font-weight: bold; fill: #ffffff; }}
    .subtitle {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 14px; fill: #8b949e; }}
    .stat-label {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 12px; fill: #8b949e; }}
    .stat-value {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 16px; font-weight: bold; fill: #ffffff; }}
    .difficulty-label {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 11px; fill: #8b949e; }}
    .difficulty-count {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 13px; font-weight: bold; fill: #ffffff; }}
    .link {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 11px; fill: #58a6ff; }}
  </style>
  
  <!-- Background -->
  <rect width="600" height="340" fill="#0d1117" rx="12" />
  
  <!-- LeetCode Logo (simplified) -->
  <circle cx="40" cy="40" r="20" fill="#ffa116" />
  <text x="40" y="46" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold" fill="#000">L</text>
  
  <!-- Username -->
  <text x="70" y="35" class="title">{LEETCODE_USERNAME}</text>
  <text x="70" y="55" class="subtitle">Global Ranking: #{ranking}</text>
  
  <!-- Total Solved Circle -->
  <circle cx="500" cy="50" r="35" fill="none" stroke="#30363d" stroke-width="6" />
  <circle cx="500" cy="50" r="35" fill="none" stroke="#ffa116" stroke-width="6" 
          stroke-dasharray="{(total_count / 500) * 220} 220" transform="rotate(-90 500 50)" />
  <text x="500" y="55" text-anchor="middle" class="stat-value" style="font-size: 18px;">{total_count}</text>
  <text x="500" y="75" text-anchor="middle" class="stat-label">Solved</text>
  
  <!-- Difficulty Progress Bars -->
  <text x="30" y="110" class="stat-label">Easy</text>
  <rect x="30" y="120" width="540" height="8" fill="#30363d" rx="4" />
  <rect x="30" y="120" width="{easy_pct * 5.4}" height="8" fill="#2ea44f" rx="4" />
  <text x="570" y="110" text-anchor="end" class="difficulty-count">{easy_count}</text>
  
  <text x="30" y="150" class="stat-label">Medium</text>
  <rect x="30" y="160" width="540" height="8" fill="#30363d" rx="4" />
  <rect x="30" y="160" width="{medium_pct * 5.4}" height="8" fill="#d29922" rx="4" />
  <text x="570" y="150" text-anchor="end" class="difficulty-count">{medium_count}</text>
  
  <text x="30" y="190" class="stat-label">Hard</text>
  <rect x="30" y="200" width="540" height="8" fill="#30363d" rx="4" />
  <rect x="30" y="200" width="{hard_pct * 5.4}" height="8" fill="#f85149" rx="4" />
  <text x="570" y="190" text-anchor="end" class="difficulty-count">{hard_count}</text>
  
  <!-- Activity Heatmap -->
  <text x="30" y="260" class="stat-label">52-Week Activity</text>
  {heatmap_cells}
  
  <!-- Date Range -->
  <text x="30" y="320" class="subtitle">{date_str}</text>
  
  <!-- Links -->
  <a href="https://leetcode.com/u/{LEETCODE_USERNAME}/" target="_blank">
    <text x="400" y="320" class="link">LeetCode Profile →</text>
  </a>
  <a href="https://github.com/AryanBhadani/DSA" target="_blank">
    <text x="520" y="320" class="link">DSA Repo →</text>
  </a>
</svg>'''
    
    return svg


def main():
    print(f"Fetching stats for {LEETCODE_USERNAME}...")
    session = get_session()
    
    # Fetch statistics
    stats = fetch_user_stats(session)
    if not stats:
        print("Failed to fetch user stats. Using fallback values.", file=sys.stderr)
        stats = {
            "matchedUser": {
                "submitStats": {"acSubmissionNum": []},
                "profile": {"ranking": "N/A"}
            }
        }
    
    # Fetch recent submissions for heatmap
    submissions = fetch_recent_submissions(session, limit=100)
    activity_weeks = generate_activity_heatmap(submissions)
    
    # Generate SVG
    svg = generate_svg(stats, activity_weeks)
    
    # Write SVG file with UTF-8 encoding
    STATS_FILE.write_text(svg, encoding='utf-8')
    print(f"Statistics card generated: {STATS_FILE}")
    
    # Write last update timestamp
    LAST_UPDATE_FILE.write_text(datetime.now().isoformat(), encoding='utf-8')
    print(f"Last update: {LAST_UPDATE_FILE.read_text()}")


if __name__ == "__main__":
    main()
