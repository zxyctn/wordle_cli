"""Adapter implementations for external dependencies.

This package contains concrete implementations of the port interfaces
defined in the domain layer.
"""

from src.wordle_cli.adapters.word_repository import InMemoryWordRepository

__all__ = ['InMemoryWordRepository']
