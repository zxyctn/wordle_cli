"""Port interfaces for the Wordle CLI domain layer.

This module defines abstract interfaces (ports) that allow the domain logic
to interact with external systems without depending on their implementations.
"""

from abc import ABC, abstractmethod


class WordRepository(ABC):
    """Abstract interface for word storage and validation."""
    
    @abstractmethod
    def get_valid_words(self) -> list[str]:
        """Return list of valid 5-letter words."""
        pass
    
    @abstractmethod
    def is_valid_word(self, word: str) -> bool:
        """Check if word exists in dictionary."""
        pass
    
    @abstractmethod
    def get_random_target(self) -> str:
        """Select a random word as the target."""
        pass
