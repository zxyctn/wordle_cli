"""GameEngine - Core game orchestration and state management.

This module implements the main game flow for Wordle, including:
- Starting new games with random target selection
- Processing guesses with validation
- Tracking game state across attempts
- Detecting win/loss conditions

The engine uses dependency injection for the word repository and
maintains immutable game state.
"""

from src.wordle_cli.domain.models import GameState, GuessResult
from src.wordle_cli.domain.ports import WordRepository
from src.wordle_cli.domain.evaluator import GuessEvaluator


class GameEngine:
    """Orchestrates Wordle game flow and state management.
    
    The engine manages the complete game lifecycle:
    1. Start new game with random target selection
    2. Validate and process guesses
    3. Track attempts and update state
    4. Detect win/loss conditions
    
    State is kept immutable - each operation returns a new GameState.
    
    Args:
        word_repo: WordRepository implementation for word validation/selection
        seed: Optional random seed for reproducible target selection (testing)
    """
    
    def __init__(self, word_repo: WordRepository):
        """Initialize game engine with word repository.
        
        Args:
            word_repo: WordRepository implementation for word operations
        """
        self._word_repo = word_repo
        self._evaluator = GuessEvaluator()
        self._state: GameState | None = None
    
    def start_new_game(self) -> GameState:
        """Start a new game with a random target word.
        
        Selects a random target word from the repository and initializes
        a fresh game state with no attempts.
        
        Returns:
            Initial GameState with selected target word
        """
        # Select random target word
        target_word = self._word_repo.get_random_target()
        
        # Create initial game state
        self._state = GameState(
            target_word=target_word.upper(),
            attempts=[],
            current_attempt=0,
            is_won=False,
            is_lost=False
        )
        
        return self._state
    
    def process_guess(self, guess: str) -> GameState:
        """Process a guess and update game state.
        
        Validates the guess, evaluates it against the target, updates
        the game state, and checks for win/loss conditions.
        
        Args:
            guess: The guessed word (5 letters, case-insensitive)
            
        Returns:
            Updated GameState after processing the guess
            
        Raises:
            ValueError: If game is over, guess is invalid length, or word
                       is not in dictionary
        """
        # Ensure game is started
        if self._state is None:
            raise ValueError("No game in progress. Call start_new_game() first.")
        
        # Check if game is already over
        if self._state.is_game_over:
            raise ValueError("Game is already over")
        
        # Validate guess length
        if len(guess) != 5:
            raise ValueError("Guess must be 5 letters")
        
        # Validate word exists in dictionary (case-insensitive)
        if not self._word_repo.is_valid_word(guess):
            raise ValueError("Invalid word")
        
        # Normalize to uppercase
        guess = guess.upper()
        
        # Evaluate the guess
        guess_result = self._evaluator.evaluate(guess, self._state.target_word)
        
        # Update attempts
        new_attempts = list(self._state.attempts) + [guess_result]
        new_attempt_number = self._state.current_attempt + 1
        
        # Check win condition
        is_won = guess_result.is_correct
        
        # Check loss condition (6 attempts used, not won)
        is_lost = new_attempt_number >= 6 and not is_won
        
        # Create new immutable state
        self._state = GameState(
            target_word=self._state.target_word,
            attempts=new_attempts,
            current_attempt=new_attempt_number,
            is_won=is_won,
            is_lost=is_lost
        )
        
        return self._state
    
    def get_current_state(self) -> GameState | None:
        """Get the current game state.
        
        Returns:
            Current GameState, or None if no game has been started
        """
        return self._state
