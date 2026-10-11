"""
test_stats.py

Unit tests for generate_stats.py - tests statistics card generation with mocked responses.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add parent directory to path to import generate_stats.py
sys.path.insert(0, str(Path(__file__).parent))

import generate_stats


class TestActivityHeatmap:
    """Test activity heatmap generation."""
    
    def test_empty_submissions(self):
        """Test heatmap with no submissions."""
        submissions = []
        weeks = generate_stats.generate_activity_heatmap(submissions)
        assert len(weeks) == 52
        assert all(w == 0 for w in weeks)
    
    def test_accepted_submissions(self):
        """Test heatmap with accepted submissions."""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        submissions = [
            {
                "title": "Two Sum",
                "statusDisplay": "Accepted",
                "timestamp": (now - timedelta(days=1)).timestamp()
            },
            {
                "title": "Add Two Numbers",
                "statusDisplay": "Accepted",
                "timestamp": (now - timedelta(days=8)).timestamp()
            }
        ]
        
        weeks = generate_stats.generate_activity_heatmap(submissions)
        assert len(weeks) == 52
        # Should have at least some non-zero values
        assert sum(weeks) > 0
    
    def test_rejected_submissions_ignored(self):
        """Test that rejected submissions are ignored."""
        submissions = [
            {
                "title": "Two Sum",
                "statusDisplay": "Wrong Answer",
                "timestamp": 1700000000
            }
        ]
        
        weeks = generate_stats.generate_activity_heatmap(submissions)
        assert all(w == 0 for w in weeks)


class TestGenerateSVG:
    """Test SVG generation."""
    
    def test_generate_svg_basic(self):
        """Test basic SVG generation."""
        stats = {
            "matchedUser": {
                "submitStats": {
                    "acSubmissionNum": [
                        {"difficulty": "Easy", "count": 50},
                        {"difficulty": "Medium", "count": 30},
                        {"difficulty": "Hard", "count": 10}
                    ]
                },
                "profile": {
                    "ranking": "10000"
                }
            }
        }
        
        activity_weeks = [0] * 52
        activity_weeks[51] = 5  # Recent activity
        
        svg = generate_stats.generate_svg(stats, activity_weeks)
        
        assert "<?xml version=" in svg
        assert "<svg" in svg
        assert "50" in svg  # Easy count
        assert "30" in svg  # Medium count
        assert "10" in svg  # Hard count
        assert "90" in svg  # Total count
        assert "10000" in svg  # Ranking
    
    def test_generate_svg_missing_fields(self):
        """Test SVG generation with missing optional fields."""
        stats = {
            "matchedUser": {
                "submitStats": {"acSubmissionNum": []},
                "profile": {"ranking": "N/A"}
            }
        }
        
        activity_weeks = [0] * 52
        svg = generate_stats.generate_svg(stats, activity_weeks)
        
        assert "<?xml version=" in svg
        assert "0" in svg  # Default counts


class TestFetchUserStats:
    """Test user stats fetching."""
    
    @patch('generate_stats.requests.Session.post')
    def test_fetch_user_stats_success(self, mock_post):
        """Test successful user stats fetch."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "data": {
                "matchedUser": {
                    "submitStats": {"acSubmissionNum": []},
                    "profile": {"ranking": "10000"}
                }
            }
        }
        mock_post.return_value = mock_response
        
        session = generate_stats.requests.Session()
        result = generate_stats.fetch_user_stats(session)
        
        assert result is not None
        assert "matchedUser" in result
    
    @patch('generate_stats.requests.Session.post')
    def test_fetch_user_stats_error(self, mock_post):
        """Test user stats fetch with GraphQL error."""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {
            "errors": [{"message": "User not found"}]
        }
        mock_post.return_value = mock_response
        
        session = generate_stats.requests.Session()
        result = generate_stats.fetch_user_stats(session)
        
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
