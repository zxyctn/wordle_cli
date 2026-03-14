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
        
        DROWN vs WORLD (W-O-R-L-D):
        - D (pos 0): present (in WORLD at position 4)
        - R (pos 1): present (in WORLD at position 2)
        - O (pos 2): present (in WORLD at position 1)
        - W (pos 3): present (in WORLD at position 0)
        - N (pos 4): absent (not in WORLD)
        """
        result = self.evaluator.evaluate("DROWN", "WORLD")
        
        assert result.guess == "DROWN"
        assert result.is_correct is False
        assert len(result.letters) == 5
        
        # All letters are in wrong positions (all PRESENT) or absent
        # D: present (in WORLD at position 4)
        assert result.letters[0].letter == "D"
        assert result.letters[0].status == LetterStatus.PRESENT
        assert result.letters[0].position == 0
        
        # R: present (in WORLD at position 2)
        assert result.letters[1].letter == "R"
        assert result.letters[1].status == LetterStatus.PRESENT
        assert result.letters[1].position == 1
        
        # O: present (in WORLD at position 1)
        assert result.letters[2].letter == "O"
        assert result.letters[2].status == LetterStatus.PRESENT
        assert result.letters[2].position == 2
        
        # W: present (in WORLD at position 0)
        assert result.letters[3].letter == "W"
        assert result.letters[3].status == LetterStatus.PRESENT
        assert result.letters[3].position == 3
        
        # N: absent (not in WORLD)
        assert result.letters[4].letter == "N"
        assert result.letters[4].status == LetterStatus.ABSENT
        assert result.letters[4].position == 4


class TestGuessEvaluatorDuplicateLetters:
    """Test duplicate letter handling - the trickiest part of Wordle logic."""
    
    def setup_method(self):
        """Create evaluator instance for each test."""
        self.evaluator = GuessEvaluator()
    
    def test_duplicate_in_guess_single_in_target(self):
        """Test duplicate letter in guess, but only one in target.
        
        ROBOT (R-O-B-O-T) vs WORLD (W-O-R-L-D):
        - R (pos 0): present (in WORLD at position 2)
        - O (pos 1): correct (matches WORLD position 1)
        - B (pos 2): absent (not in WORLD)
        - O (pos 3): absent (O already used in position 1)
        - T (pos 4): absent (not in WORLD)
        
        Critical: Second O should be ABSENT because target only has one O
        and it was already matched in position 1 (CORRECT).
        """
        result = self.evaluator.evaluate("ROBOT", "WORLD")
        
        assert result.guess == "ROBOT"
        assert result.is_correct is False
        
        # R: present (in WORLD at position 2)
        assert result.letters[0].letter == "R"
        assert result.letters[0].status == LetterStatus.PRESENT
        
        # O: correct (position 1)
        assert result.letters[1].letter == "O"
        assert result.letters[1].status == LetterStatus.CORRECT
        
        # B: absent
        assert result.letters[2].letter == "B"
        assert result.letters[2].status == LetterStatus.ABSENT
        
        # O: absent (already used)
        assert result.letters[3].letter == "O"
        assert result.letters[3].status == LetterStatus.ABSENT
        
        # T: absent
        assert result.letters[4].letter == "T"
        assert result.letters[4].status == LetterStatus.ABSENT
    
    def test_multiple_same_letter_in_guess(self):
        """Test multiple instances of same letter in guess.
        
        SPEED (S-P-E-E-D) vs CREEP (C-R-E-E-P):
        - S (pos 0): absent (not in CREEP)
        - P (pos 1): present (in CREEP at position 4)
        - E (pos 2): correct (matches CREEP position 2)
        - E (pos 3): correct (matches CREEP position 3)
        - D (pos 4): absent (not in CREEP)
        """
        result = self.evaluator.evaluate("SPEED", "CREEP")
        
        assert result.guess == "SPEED"
        assert result.is_correct is False
        
        # S: absent
        assert result.letters[0].status == LetterStatus.ABSENT
        
        # P: present (in CREEP at position 4)
        assert result.letters[1].letter == "P"
        assert result.letters[1].status == LetterStatus.PRESENT
        
        # E: correct
        assert result.letters[2].letter == "E"
        assert result.letters[2].status == LetterStatus.CORRECT
        
        # E: correct
        assert result.letters[3].letter == "E"
        assert result.letters[3].status == LetterStatus.CORRECT
        
        # D: absent
        assert result.letters[4].status == LetterStatus.ABSENT
    
    def test_duplicate_L_in_guess(self):
        """Test duplicate L in guess with single L in target.
        
        LLAMA (L-L-A-M-A) vs WORLD (W-O-R-L-D):
        - L (pos 0): present (in WORLD at position 3)
        - L (pos 1): absent (only one L in WORLD, already used)
        - A (pos 2): absent (not in WORLD)
        - M (pos 3): absent (not in WORLD)
        - A (pos 4): absent (not in WORLD)
        """
        result = self.evaluator.evaluate("LLAMA", "WORLD")
        
        assert result.guess == "LLAMA"
        assert result.is_correct is False
        
        # First L: present (in WORLD at position 3)
        assert result.letters[0].letter == "L"
        assert result.letters[0].status == LetterStatus.PRESENT
        
        # Second L: absent (already used)
        assert result.letters[1].letter == "L"
        assert result.letters[1].status == LetterStatus.ABSENT
        
        # Rest are absent
        assert result.letters[2].status == LetterStatus.ABSENT
        assert result.letters[3].status == LetterStatus.ABSENT
        assert result.letters[4].status == LetterStatus.ABSENT
    
    def test_single_in_guess_duplicate_in_target(self):
        """Test single letter in guess with duplicate in target.
        
        SWORD (S-W-O-R-D) vs ROBOT (R-O-B-O-T):
        - S (pos 0): absent (not in ROBOT)
        - W (pos 1): absent (not in ROBOT)
        - O (pos 2): present (ROBOT has O at positions 1 and 3)
        - R (pos 3): present (in ROBOT at position 0)
        - D (pos 4): absent (not in ROBOT)
        """
        result = self.evaluator.evaluate("SWORD", "ROBOT")
        
        assert result.guess == "SWORD"
        assert result.is_correct is False
        
        # S: absent
        assert result.letters[0].status == LetterStatus.ABSENT
        
        # W: absent
        assert result.letters[1].status == LetterStatus.ABSENT
        
        # O: present (matches one of the Os in ROBOT)
        assert result.letters[2].letter == "O"
        assert result.letters[2].status == LetterStatus.PRESENT
        
        # R: present
        assert result.letters[3].letter == "R"
        assert result.letters[3].status == LetterStatus.PRESENT
        
        # D: absent
        assert result.letters[4].status == LetterStatus.ABSENT
    
    def test_complex_duplicate_scenario(self):
        """Test complex scenario with multiple duplicate E's.
        
        TEPEE (T-E-P-E-E) vs CREEP (C-R-E-E-P):
        - T (pos 0): absent (not in CREEP)
        - E (pos 1): present (CREEP has E at positions 2 and 3)
        - P (pos 2): present (in CREEP at position 4)
        - E (pos 3): correct (matches CREEP position 3)
        - E (pos 4): absent (CREEP only has 2 E's, both used)
        
        Note: First E gets PRESENT, third E gets CORRECT, fourth E is ABSENT.
        """
        result = self.evaluator.evaluate("TEPEE", "CREEP")
        
        assert result.guess == "TEPEE"
        assert result.is_correct is False
        
        # T: absent
        assert result.letters[0].status == LetterStatus.ABSENT
        
        # E: present (one of CREEP's E's)
        assert result.letters[1].letter == "E"
        assert result.letters[1].status == LetterStatus.PRESENT
        
        # P: present (in CREEP at position 4)
        assert result.letters[2].letter == "P"
        assert result.letters[2].status == LetterStatus.PRESENT
        
        # E: correct (matches position 3)
        assert result.letters[3].letter == "E"
        assert result.letters[3].status == LetterStatus.CORRECT
        
        # E: absent (both CREEP E's already used)
        assert result.letters[4].letter == "E"
        assert result.letters[4].status == LetterStatus.ABSENT
    
    def test_correct_priority_over_present(self):
        """Test that CORRECT takes priority over PRESENT.
        
        LLAMA (L-L-A-M-A) vs SALAL (S-A-L-A-L):
        - L (pos 0): present (SALAL has L at positions 2 and 4)
        - L (pos 1): present (second L in SALAL)
        - A (pos 2): correct (matches SALAL position 2)... wait, no.
        
        Let me recalculate: SALAL = S-A-L-A-L
        - L (pos 0): present (in SALAL at positions 2, 4)
        - L (pos 1): present (second L in SALAL)
        - A (pos 2): present (SALAL has A at positions 1, 3)
        - M (pos 3): absent
        - A (pos 4): present (second A in SALAL)
        
        Actually, let me use a better example for priority testing.
        
        ALLAY (A-L-L-A-Y) vs SALAL (S-A-L-A-L):
        - A (pos 0): present (in SALAL at positions 1, 3)
        - L (pos 1): present (in SALAL at positions 2, 4)
        - L (pos 2): correct (matches SALAL position 2)
        - A (pos 3): correct (matches SALAL position 3)
        - Y (pos 4): absent (not in SALAL)
        
        This tests that when L appears at positions 1 and 2 in guess,
        and position 2 is CORRECT, position 1 gets PRESENT from remaining L.
        """
        result = self.evaluator.evaluate("ALLAY", "SALAL")
        
        assert result.guess == "ALLAY"
        assert result.is_correct is False
        
        # A (pos 0): present
        assert result.letters[0].letter == "A"
        assert result.letters[0].status == LetterStatus.PRESENT
        
        # L (pos 1): present
        assert result.letters[1].letter == "L"
        assert result.letters[1].status == LetterStatus.PRESENT
        
        # L (pos 2): correct
        assert result.letters[2].letter == "L"
        assert result.letters[2].status == LetterStatus.CORRECT
        
        # A (pos 3): correct
        assert result.letters[3].letter == "A"
        assert result.letters[3].status == LetterStatus.CORRECT
        
        # Y (pos 4): absent
        assert result.letters[4].letter == "Y"
        assert result.letters[4].status == LetterStatus.ABSENT
