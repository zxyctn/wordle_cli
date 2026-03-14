"""Domain layer - core game models and port interfaces."""

from .models import GameState, GuessResult, LetterResult, LetterStatus
from .ports import WordRepository
from .evaluator import GuessEvaluator
from .game_engine import GameEngine

__all__ = [
    "LetterStatus",
    "LetterResult",
    "GuessResult",
    "GameState",
    "WordRepository",
    "GuessEvaluator",
    "GameEngine",
]
