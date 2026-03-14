"""GuessEvaluator - Core Wordle guess evaluation logic.

This module implements the core algorithm for comparing a guess against
a target word and determining which letters are correct, present, or absent.

The two-pass algorithm correctly handles duplicate letters:
1. First pass: Mark CORRECT positions and consume target letters
2. Second pass: Mark PRESENT from remaining target letters, rest ABSENT
"""

from collections import Counter
from src.wordle_cli.domain.models import LetterStatus, LetterResult, GuessResult


class GuessEvaluator:
    """Evaluates guesses against target words using Wordle rules.
    
    The evaluator uses a two-pass algorithm to correctly handle duplicate
    letters in both the guess and target word:
    
    1. First pass: Mark all CORRECT positions (exact matches)
    2. Second pass: Mark PRESENT for letters that exist in target but
       are in wrong position, ABSENT for letters not in target
    
    This ensures that duplicate letters are evaluated independently and
    that CORRECT status takes priority over PRESENT.
    """
    
    def evaluate(self, guess: str, target: str) -> GuessResult:
        """Evaluate a guess against a target word.
        
        Args:
            guess: The guessed word (5 letters)
            target: The target word to compare against (5 letters)
            
        Returns:
            GuessResult containing evaluation for each letter
        """
        # Normalize to uppercase for comparison
        guess = guess.upper()
        target = target.upper()
        
        # Count available letters in target (for duplicate handling)
        target_letter_counts = Counter(target)
        
        # Initialize results - all ABSENT by default
        results = [
            LetterResult(
                letter=guess[i],
                status=LetterStatus.ABSENT,
                position=i
            )
            for i in range(5)
        ]
        
        # First pass: Mark CORRECT positions and consume target letters
        for i in range(5):
            if guess[i] == target[i]:
                results[i] = LetterResult(
                    letter=guess[i],
                    status=LetterStatus.CORRECT,
                    position=i
                )
                # Consume this letter from target counts
                target_letter_counts[guess[i]] -= 1
        
        # Second pass: Mark PRESENT from remaining target letters
        for i in range(5):
            # Skip if already marked CORRECT
            if results[i].status == LetterStatus.CORRECT:
                continue
            
            # Check if this letter is still available in target
            if target_letter_counts[guess[i]] > 0:
                results[i] = LetterResult(
                    letter=guess[i],
                    status=LetterStatus.PRESENT,
                    position=i
                )
                # Consume this letter from target counts
                target_letter_counts[guess[i]] -= 1
            # else: remains ABSENT (default from initialization)
        
        # Check if guess is completely correct
        is_correct = all(result.status == LetterStatus.CORRECT for result in results)
        
        return GuessResult(
            guess=guess,
            letters=results,
            is_correct=is_correct
        )
