"""In-memory implementation of the WordRepository port.

This adapter loads words from the words.py module and provides
in-memory storage with O(1) validation lookups. Supports seeded
random selection for reproducible testing.
"""

import random
from wordle_cli.words import game_words
from src.wordle_cli.domain.ports import WordRepository


class InMemoryWordRepository(WordRepository):
    """Word repository that loads words from words.py module.
    
    This adapter provides:
    - Fast O(1) word validation using a set
    - Reproducible random word selection via seeding
    - Case-insensitive word validation
    
    Args:
        seed: Optional random seed for reproducible target selection.
              Use for testing to get consistent results.
    """
    
    def __init__(self, seed: int | None = None):
        """Initialize repository with words from words.py.
        
        Args:
            seed: Optional seed for random number generator.
                  If provided, get_random_target() will be reproducible.
        """
        self._words = game_words
        self._word_set = set(word.lower() for word in game_words)
        self._random = random.Random(seed)
    
    def get_valid_words(self) -> list[str]:
        """Return list of valid 5-letter words.
        
        Returns:
            List of all valid words from the game dictionary.
        """
        return self._words
    
    def is_valid_word(self, word: str) -> bool:
        """Check if word exists in dictionary (case-insensitive).
        
        Args:
            word: Word to validate.
            
        Returns:
            True if word exists in the dictionary, False otherwise.
        """
        return word.lower() in self._word_set
    
    def get_random_target(self) -> str:
        """Select a random word as the target.
        
        Uses the seeded random generator if seed was provided during
        initialization, ensuring reproducible results for testing.
        
        Returns:
            A randomly selected word from the valid word list.
        """
        return self._random.choice(self._words)
