"""
Unit tests for the scoring engine.
Tests all risk categories: Low, Medium, High, Critical.
"""
from backend.engines.scoring import calculate_score


class TestCalculateScore:
    """Tests for calculate_score function."""

    def test_safe_prompt_scores_low(self):
        detection = {"is_malicious": False, "patterns_detected": []}
        result = calculate_score(detection)
        assert result["score"] == 0
        assert result["category"] == "Low"

    def test_one_pattern_scores_high(self):
        """One pattern: score = 50 + (1 * 20) = 70 → High"""
        detection = {"is_malicious": True, "patterns_detected": ["ignore previous instructions"]}
        result = calculate_score(detection)
        assert result["score"] == 70
        assert result["category"] == "High"

    def test_two_patterns_scores_critical(self):
        """Two patterns: score = 50 + (2 * 20) = 90 → Critical"""
        detection = {"is_malicious": True, "patterns_detected": ["ignore previous instructions", "bypass safety"]}
        result = calculate_score(detection)
        assert result["score"] == 90
        assert result["category"] == "Critical"

    def test_three_patterns_caps_at_100(self):
        """Three patterns: score = min(100, 50 + 60) = 100 → Critical"""
        detection = {
            "is_malicious": True,
            "patterns_detected": ["ignore previous instructions", "bypass safety", "do anything now"]
        }
        result = calculate_score(detection)
        assert result["score"] == 100
        assert result["category"] == "Critical"

    def test_score_capped_at_100(self):
        """Five patterns: score = min(100, 50 + 100) = 100"""
        detection = {
            "is_malicious": True,
            "patterns_detected": ["a", "b", "c", "d", "e"]
        }
        result = calculate_score(detection)
        assert result["score"] == 100

    def test_category_boundaries(self):
        """Verify category boundaries are correct."""
        # Low: 0-20
        assert calculate_score({"is_malicious": False, "patterns_detected": []})["category"] == "Low"
        # High: 61-80 (1 pattern = 70)
        assert calculate_score({"is_malicious": True, "patterns_detected": ["a"]})["category"] == "High"
        # Critical: 81-100 (2 patterns = 90)
        assert calculate_score({"is_malicious": True, "patterns_detected": ["a", "b"]})["category"] == "Critical"
