"""Tests for GuessEvaluator - letter status evaluation logic.

This module contains comprehensive tests for the core Wordle evaluation
algorithm, especially focusing on the tricky duplicate letter handling.
"""

import pytest
from src.wordle_cli.domain.evaluator import GuessEvaluator
from src.wordle_cli.domain.models import LetterStatus, GuessResult


class TestGuessEvaluatorSimpleCases:
    """Test simple evaluation cases without duplicate letters."""
    
    def setup_method(self):
        """Create evaluator instance for each test."""
        self.evaluator = GuessEvaluator()
    
    def test_all_correct(self):
        """Test when all letters match in correct positions."""
        result = self.evaluator.evaluate("WORLD", "WORLD")
        
        assert isinstance(result, GuessResult)
        assert result.guess == "WORLD"
        assert result.is_correct is True
        assert len(result.letters) == 5
        
        # All letters should be CORRECT
        for i, letter_result in enumerate(result.letters):
            assert letter_result.letter == "WORLD"[i]
            assert letter_result.status == LetterStatus.CORRECT
            assert letter_result.position == i
    
    def test_all_absent(self):
        """Test when no letters are in the target word."""
        result = self.evaluator.evaluate("BRICK", "LOAMY")
        
        assert isinstance(result, GuessResult)
        assert result.guess == "BRICK"
        assert result.is_correct is False
        assert len(result.letters) == 5
        
        # All letters should be ABSENT
        for i, letter_result in enumerate(result.letters):
            assert letter_result.letter == "BRICK"[i]
            assert letter_result.status == LetterStatus.ABSENT
            assert letter_result.position == i
    
    def test_mixed_positions(self):
        """Test mixed correct, present, and absent letters.
        
        DROWN vs WORLD:
        - D: present (in WORLD at position 4)
        - R: correct (position 1)
        - O: correct (position 1)
        - W: present (in WORLD at position 0)
        - N: absent (not in WORLD)
        """
        result = self.evaluator.evaluate("DROWN", "WORLD")
        
        assert result.guess == "DROWN"
        assert result.is_correct is False
        assert len(result.letters) == 5
        
        # D: present (in WORLD at position 4)
        assert result.letters[0].letter == "D"
        assert result.letters[0].status == LetterStatus.PRESENT
        assert result.letters[0].position == 0
        
        # R: correct (position 1)
        assert result.letters[1].letter == "R"
        assert result.letters[1].status == LetterStatus.CORRECT
        assert result.letters[1].position == 1
        
        # O: correct (position 2)
        assert result.letters[2].letter == "O"
        assert result.letters[2].status == LetterStatus.CORRECT
        assert result.letters[2].position == 2
        
        # W: present (in WORLD at position 0)
        assert result.letters[3].letter == "W"
        assert result.letters[3].status == LetterStatus.PRESENT
        assert result.letters[3].position == 3
        
        # N: absent (not in WORLD)
        assert result.letters[4].letter == "N"
        assert result.letters[4].status == LetterStatus.ABSENT
        assert result.letters[4].position == 4
