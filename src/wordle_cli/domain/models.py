"""Domain models for Wordle game.

This module contains pure Python domain models with zero external dependencies.
All models are immutable (frozen dataclasses) for predictable state management.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class LetterStatus(Enum):
    """Status of a letter in a guess relative to the target word."""
    
    CORRECT = "correct"  # Green - right letter, right position
    PRESENT = "present"  # Yellow - right letter, wrong position
    ABSENT = "absent"    # Gray - letter not in word


@dataclass(frozen=True)
class LetterResult:
    """Evaluation result for a single letter in a guess.
    
    Attributes:
        letter: The guessed letter (single character)
        status: Evaluation status (correct/present/absent)
        position: Position in the word (0-4 for 5-letter words)
    """
    
    letter: str
    status: LetterStatus
    position: int


@dataclass(frozen=True)
class GuessResult:
    """Complete evaluation result for a 5-letter guess.
    
    Attributes:
        guess: The complete guessed word (5 letters)
        letters: List of evaluation results for each letter
        is_correct: True if all letters are CORRECT
    """
    
    guess: str
    letters: List[LetterResult]
    is_correct: bool


@dataclass(frozen=True)
class GameState:
    """Complete state of a Wordle game.
    
    Attributes:
        target_word: The secret word to guess (5 letters)
        attempts: List of guess results so far (max 6)
        current_attempt: Current attempt number (0-6)
        is_won: True if player guessed correctly
        is_lost: True if player used all 6 attempts without winning
    """
    
    target_word: str
    attempts: List[GuessResult]
    current_attempt: int
    is_won: bool
    is_lost: bool
    
    def __post_init__(self):
        """Validate that current_attempt matches attempts list."""
        if self.current_attempt != len(self.attempts):
            raise ValueError(
                f"current_attempt ({self.current_attempt}) must match "
                f"len(attempts) ({len(self.attempts)})"
            )
    
    @property
    def is_game_over(self) -> bool:
        """Returns True if the game has ended (won or lost)."""
        return self.is_won or self.is_lost
