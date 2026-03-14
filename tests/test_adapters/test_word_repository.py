"""Integration tests for InMemoryWordRepository adapter.

Tests verify that the adapter correctly loads words from words.py
and implements all WordRepository interface methods.
"""

import pytest
from src.wordle_cli.adapters import InMemoryWordRepository


class TestInMemoryWordRepository:
    """Test suite for InMemoryWordRepository adapter."""
    
    def test_loads_words_from_file(self):
        """Verify get_valid_words() returns list with expected count."""
        repo = InMemoryWordRepository()
        words = repo.get_valid_words()
        
        assert isinstance(words, list)
        assert len(words) > 1000, "Expected >1000 words from words.py"
        # Verify all words are 5 letters (spot check)
        assert all(len(word) == 5 for word in words[:100])
    
    def test_validates_valid_words(self):
        """Test is_valid_word() returns True for known words."""
        repo = InMemoryWordRepository()
        
        # Test multiple known valid words
        assert repo.is_valid_word("world")
        assert repo.is_valid_word("robot")
        assert repo.is_valid_word("audio")
    
    def test_rejects_invalid_words(self):
        """Test is_valid_word() returns False for nonsense."""
        repo = InMemoryWordRepository()
        
        # Test various invalid inputs
        assert not repo.is_valid_word("xyzqk")
        assert not repo.is_valid_word("aaaaa")
        assert not repo.is_valid_word("12345")
    
    def test_case_insensitive_validation(self):
        """Verify different cases all validate as True."""
        repo = InMemoryWordRepository()
        
        # Same word in different cases should all be valid
        assert repo.is_valid_word("WORLD")
        assert repo.is_valid_word("World")
        assert repo.is_valid_word("world")
        assert repo.is_valid_word("wOrLd")
    
    def test_random_target_selection(self):
        """Verify get_random_target() returns 5-letter word from valid list."""
        repo = InMemoryWordRepository()
        valid_words = repo.get_valid_words()
        
        # Get a random target
        target = repo.get_random_target()
        
        assert isinstance(target, str)
        assert len(target) == 5
        assert target in valid_words
    
    def test_seeded_random_reproducible(self):
        """Create two repos with same seed, verify identical results."""
        repo1 = InMemoryWordRepository(seed=42)
        repo2 = InMemoryWordRepository(seed=42)
        
        # Get targets from both repos
        target1 = repo1.get_random_target()
        target2 = repo2.get_random_target()
        
        # Should be identical with same seed
        assert target1 == target2
        
        # Multiple calls should also match
        for _ in range(5):
            assert repo1.get_random_target() == repo2.get_random_target()
    
    def test_different_seeds_likely_different(self):
        """Create repos with different seeds, verify at least 1 difference."""
        repo1 = InMemoryWordRepository(seed=42)
        repo2 = InMemoryWordRepository(seed=123)
        
        # Collect targets from both repos
        targets1 = [repo1.get_random_target() for _ in range(10)]
        targets2 = [repo2.get_random_target() for _ in range(10)]
        
        # With different seeds, at least one should differ (probabilistic)
        # With 17K+ words and 10 samples, probability of all matching is negligible
        assert targets1 != targets2, "Different seeds should produce different sequences"
