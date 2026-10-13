"""
Match audited solutions with LeetCode data and prepare migration preview.
"""

import json
from pathlib import Path
from datetime import datetime

AUDIT_FILE = Path(r"C:\Users\vikas\CascadeProjects\DSA-Fresh\audit_report.json")
BASELINE_FILE = Path(r"C:\Users\vikas\CascadeProjects\DSA-Fresh\baseline_stats.json")
RECENT_SUBMISSIONS_FILE = Path(r"C:\Users\vikas\CascadeProjects\DSA-Fresh\recent_submissions.json")

def load_json(file_path):
    """Load JSON file if it exists."""
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return None

def prepare_migration_preview():
    """Create migration preview matching audit data with LeetCode data."""
    
    audit_data = load_json(AUDIT_FILE)
    baseline_data = load_json(BASELINE_FILE)
    
    if not audit_data:
        print("ERROR: Audit report not found", file=open(2))
        return None
    
    # Load recent submissions if available
    recent_submissions = []
    if RECENT_SUBMISSIONS_FILE.exists():
        with open(RECENT_SUBMISSIONS_FILE, 'r') as f:
            data = json.load(f)
            recent_submissions = data.get("data", {}).get("recentSubmissionList", [])
    
    # Create slug lookup from recent submissions
    recent_slugs = {sub["titleSlug"]: sub for sub in recent_submissions}
    
    migration_preview = {
        "preview_timestamp": datetime.utcnow().isoformat(),
        "baseline_statistics": baseline_data,
        "audited_solutions_count": len(audit_data["solutions"]),
        "recent_submissions_count": len(recent_submissions),
        "migration_candidates": []
    }
    
    # Match each audited solution
    for solution in audit_data["solutions"]:
        title_slug = solution["title_slug"]
        folder_name = solution["folder_name"]
        
        migration_item = {
            "folder_name": folder_name,
            "problem_id": solution["problem_id"],
            "title_slug": title_slug,
            "has_cpp": solution["has_cpp"],
            "has_readme": solution["has_readme"],
            "tracker_submission_id": solution.get("tracker_entry", {}).get("submission_id"),
            "in_recent_submissions": title_slug in recent_slugs,
            "recent_submission": recent_slugs.get(title_slug) if title_slug in recent_slugs else None,
            "verification_status": solution["verification_status"],
            "migration_recommended": True,
            "notes": []
        }
        
        # Add notes based on analysis
        if not solution["has_cpp"]:
            migration_item["migration_recommended"] = False
            migration_item["notes"].append("No C++ solution file found")
        
        if not solution["has_readme"]:
            migration_item["notes"].append("Missing README.md")
        
        if title_slug in recent_slugs:
            recent = recent_slugs[title_slug]
            if recent.get("statusDisplay") == "Accepted" and recent.get("lang") == "cpp":
                migration_item["notes"].append("Recently solved in C++")
            elif recent.get("statusDisplay") != "Accepted":
                migration_item["notes"].append(f"Recent status: {recent.get('statusDisplay')}")
        
        migration_preview["migration_candidates"].append(migration_item)
    
    # Save migration preview
    output_file = Path(r"C:\Users\vikas\CascadeProjects\DSA-Fresh\migration_preview.json")
    with open(output_file, 'w') as f:
        json.dump(migration_preview, f, indent=2)
    
    print(f"Migration preview saved to: {output_file}")
    
    # Print summary
    recommended_count = sum(1 for item in migration_preview["migration_candidates"] if item["migration_recommended"])
    print(f"\nMigration Summary:")
    print(f"  Total audited solutions: {migration_preview['audited_solutions_count']}")
    print(f"  Recommended for migration: {recommended_count}")
    print(f"  Not recommended: {migration_preview['audited_solutions_count'] - recommended_count}")
    
    in_recent = sum(1 for item in migration_preview["migration_candidates"] if item["in_recent_submissions"])
    print(f"  Found in recent submissions: {in_recent}")
    
    return migration_preview

if __name__ == "__main__":
    print("=" * 60)
    print("Preparing Migration Preview")
    print("=" * 60)
    
    preview = prepare_migration_preview()
    
    print("\n" + "=" * 60)
    print("Migration Preview Complete")
    print("=" * 60)
