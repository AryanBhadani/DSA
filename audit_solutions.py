"""
Audit existing solutions from the old DSA directory.
Read-only inspection - no modifications to original files.
"""

import os
import json
from pathlib import Path
from datetime import datetime

OLD_DIR = Path(r"C:\Users\vikas\CascadeProjects\DSA")
PROBLEMS_DIR = OLD_DIR / "problems"
TRACKER_FILE = OLD_DIR / "synced_submissions.json"

def audit_solutions():
    """Inspect all existing solutions and create an audit report."""
    
    # Load the tracker
    tracker_data = {}
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE, 'r') as f:
            tracker_data = json.load(f)
    
    audit_report = {
        "audit_timestamp": datetime.utcnow().isoformat(),
        "source_directory": str(OLD_DIR),
        "problems_directory": str(PROBLEMS_DIR),
        "tracker_entries": len(tracker_data),
        "solutions": []
    }
    
    # Count problem folders
    if PROBLEMS_DIR.exists():
        problem_folders = [d for d in PROBLEMS_DIR.iterdir() if d.is_dir()]
        audit_report["problem_folders_count"] = len(problem_folders)
        
        for folder in sorted(problem_folders):
            folder_name = folder.name
            
            # Check for solution files
            solution_files = list(folder.glob("solution.*"))
            cpp_files = list(folder.glob("*.cpp"))
            
            # Check for README
            readme_file = folder / "README.md"
            has_readme = readme_file.exists()
            
            # Extract problem info from folder name
            # Format: "id-title-slug"
            parts = folder_name.split("-", 1)
            problem_id = parts[0] if len(parts) > 0 else "unknown"
            title_slug = parts[1] if len(parts) > 1 else "unknown"
            
            # Check tracker for this problem
            tracker_entry = None
            for key, value in tracker_data.items():
                if value.get("folder") == folder_name:
                    tracker_entry = {"key": key, "submission_id": value.get("submission_id")}
                    break
            
            solution_info = {
                "folder_name": folder_name,
                "problem_id": problem_id,
                "title_slug": title_slug,
                "has_solution": len(solution_files) > 0,
                "solution_files": [f.name for f in solution_files],
                "has_cpp": len(cpp_files) > 0,
                "cpp_files": [f.name for f in cpp_files],
                "has_readme": has_readme,
                "tracker_entry": tracker_entry,
                "verification_status": "pending"
            }
            
            # Basic verification checks
            if not solution_files:
                solution_info["verification_status"] = "missing_solution"
            elif not cpp_files:
                solution_info["verification_status"] = "no_cpp"
            elif not has_readme:
                solution_info["verification_status"] = "missing_readme"
            elif not tracker_entry:
                solution_info["verification_status"] = "not_in_tracker"
            else:
                solution_info["verification_status"] = "needs_review"
            
            audit_report["solutions"].append(solution_info)
    
    # Save audit report
    output_file = Path(r"C:\Users\vikas\CascadeProjects\DSA-Fresh\audit_report.json")
    with open(output_file, 'w') as f:
        json.dump(audit_report, f, indent=2)
    
    print(f"Audit complete. Report saved to: {output_file}")
    print(f"Total solutions audited: {len(audit_report['solutions'])}")
    
    # Print summary
    status_counts = {}
    for sol in audit_report["solutions"]:
        status = sol["verification_status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nVerification Status Summary:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    return audit_report

if __name__ == "__main__":
    print("=" * 60)
    print("Auditing Existing Solutions (Read-Only)")
    print("=" * 60)
    
    report = audit_solutions()
    
    print("\n" + "=" * 60)
    print("Audit Complete")
    print("=" * 60)
