"""Port interfaces for external dependencies.

This module defines abstract interfaces following hexagonal architecture.
Domain logic depends on these abstractions, not concrete implementations.
"""

from abc import ABC, abstractmethod


class WordRepository(ABC):
    """Abstract interface for word dictionary operations.
    
    Implementations provide access to valid 5-letter words for the game.
    This port enables dependency inversion - domain logic stays pure while
    adapters can load words from files, APIs, or other sources.
    """
    
    @abstractmethod
    def get_valid_words(self) -> list[str]:
        """Return all valid 5-letter words that can be guessed.
        
        Returns:
            List of valid 5-letter words in lowercase
        """
        pass
    
    @abstractmethod
    def is_valid_word(self, word: str) -> bool:
        """Check if a word exists in the valid word dictionary.
        
        Args:
            word: The word to validate (should be 5 letters)
            
        Returns:
            True if word is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_random_target(self) -> str:
        """Select a random word to use as the target word.
        
        Returns:
            A random 5-letter word from the valid word list
        """
        pass
