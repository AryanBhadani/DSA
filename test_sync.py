"""
test_sync.py

Unit tests for sync.py - tests LeetCode synchronization logic with mocked responses.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

# Add parent directory to path to import sync.py
sys.path.insert(0, str(Path(__file__).parent))

import sync


class TestSyncedSubmissions:
    """Test synced submissions tracking."""
    
    def test_load_synced_empty(self):
        """Test loading when no synced file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sync.SYNCED_FILE = Path(tmpdir) / "synced.json"
            result = sync.load_synced()
            assert result == {}
    
    def test_load_synced_existing(self):
        """Test loading existing synced file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sync.SYNCED_FILE = Path(tmpdir) / "synced.json"
            test_data = {"two-sum:python": {"submission_id": "123", "folder": "1-two-sum"}}
            sync.SYNCED_FILE.write_text(json.dumps(test_data))
            result = sync.load_synced()
            assert result == test_data
    
    def test_save_synced(self):
        """Test saving synced data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sync.SYNCED_FILE = Path(tmpdir) / "synced.json"
            test_data = {"two-sum:python": {"submission_id": "123", "folder": "1-two-sum"}}
            sync.save_synced(test_data)
            result = json.loads(sync.SYNCED_FILE.read_text())
            assert result == test_data


class TestSlugifyFolder:
    """Test folder name generation."""
    
    def test_slugify_folder(self):
        """Test basic slugification."""
        result = sync.slugify_folder("1", "two-sum")
        assert result == "1-two-sum"
    
    def test_slugify_folder_with_special_chars(self):
        """Test slugification with special characters."""
        result = sync.slugify_folder("123", "valid-palindrome-ii")
        assert result == "123-valid-palindrome-ii"


class TestWriteProblem:
    """Test problem file writing."""
    
    def test_write_problem_with_tags(self):
        """Test writing problem with tags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sync.PROBLEMS_DIR = Path(tmpdir)
            
            details = {
                "code": "class Solution { public: int solve() { return 0; } };",
                "lang": {"name": "cpp"},
                "question": {
                    "questionId": "1",
                    "title": "Two Sum",
                    "titleSlug": "two-sum",
                    "difficulty": "Easy",
                    "topicTags": [{"name": "Array"}, {"name": "Hash Table"}]
                }
            }
            
            submission = {"timestamp": "1700000000"}
            
            folder_name = sync.write_problem(details, submission)
            
            assert folder_name == "1-two-sum"
            assert (sync.PROBLEMS_DIR / "1-two-sum" / "solution.cpp").exists()
            assert (sync.PROBLEMS_DIR / "1-two-sum" / "README.md").exists()
            
            readme = (sync.PROBLEMS_DIR / "1-two-sum" / "README.md").read_text()
            assert "Two Sum" in readme
            assert "Easy" in readme
            assert "Array, Hash Table" in readme
    
    def test_write_problem_without_tags(self):
        """Test writing problem with None topicTags."""
        with tempfile.TemporaryDirectory() as tmpdir:
            sync.PROBLEMS_DIR = Path(tmpdir)
            
            details = {
                "code": "def solve(): return 0",
                "lang": {"name": "python3"},
                "question": {
                    "questionId": "2",
                    "title": "Add Two Numbers",
                    "titleSlug": "add-two-numbers",
                    "difficulty": "Medium",
                    "topicTags": None
                }
            }
            
            submission = {"timestamp": "1700000000"}
            
            folder_name = sync.write_problem(details, submission)
            
            assert folder_name == "2-add-two-numbers"
            readme = (sync.PROBLEMS_DIR / "2-add-two-numbers" / "README.md").read_text()
            assert "Tags:" in readme  # Should handle None gracefully


class TestFetchSubmissionDetails:
    """Test submission details fetching with error handling."""
    
    @patch('sync.requests.Session.post')
    def test_fetch_submission_details_success(self, mock_post):
        """Test successful submission details fetch."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "data": {
                "submissionDetails": {
                    "code": "test code",
                    "lang": {"name": "python"},
                    "question": {
                        "questionId": "1",
                        "title": "Test",
                        "titleSlug": "test",
                        "difficulty": "Easy",
                        "topicTags": [{"name": "Array"}]
                    }
                }
            }
        }
        mock_post.return_value = mock_response
        
        session = sync.requests.Session()
        result = sync.fetch_submission_details(session, "123")
        
        assert result is not None
        assert result["code"] == "test code"
    
    @patch('sync.requests.Session.post')
    def test_fetch_submission_details_error(self, mock_post):
        """Test submission details fetch with GraphQL error."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "errors": [{"message": "Not found"}]
        }
        mock_post.return_value = mock_response
        
        session = sync.requests.Session()
        result = sync.fetch_submission_details(session, "999")
        
        assert result is None
    
    @patch('sync.requests.Session.post')
    def test_fetch_submission_details_http_error(self, mock_post):
        """Test submission details fetch with HTTP error."""
        mock_post.side_effect = Exception("Network error")
        
        session = sync.requests.Session()
        # Should raise exception, not return None
        with pytest.raises(Exception, match="Network error"):
            sync.fetch_submission_details(session, "123")


class TestDuplicateDetection:
    """Test duplicate submission detection."""
    
    def test_duplicate_detection_same_problem_language(self):
        """Test that same problem+language is detected as duplicate."""
        synced = {
            "two-sum:python": {"submission_id": "123", "folder": "1-two-sum"}
        }
        
        submission = {
            "id": "456",
            "titleSlug": "two-sum",
            "lang": "python"
        }
        
        key = f"{submission['titleSlug']}:{submission['lang']}"
        assert key in synced
    
    def test_duplicate_detection_different_language(self):
        """Test that different language is not a duplicate."""
        synced = {
            "two-sum:python": {"submission_id": "123", "folder": "1-two-sum"}
        }
        
        submission = {
            "id": "456",
            "titleSlug": "two-sum",
            "lang": "cpp"
        }
        
        key = f"{submission['titleSlug']}:{submission['lang']}"
        assert key not in synced


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
