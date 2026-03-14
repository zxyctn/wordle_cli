"""Tests for GameEngine - game orchestration and state management.

This module tests the core game flow including word validation,
attempt tracking, and win/loss condition detection.
"""

import pytest
from src.wordle_cli.domain.game_engine import GameEngine
from src.wordle_cli.domain.models import GameState, LetterStatus
from src.wordle_cli.adapters.word_repository import InMemoryWordRepository


class TestGameEngine:
    """Test GameEngine orchestration and state management."""
    
    def setup_method(self):
        """Create engine with seeded repository for reproducible tests."""
        # Use seeded repository so we know what the target word will be
        self.word_repo = InMemoryWordRepository(seed=42)
        self.engine = GameEngine(self.word_repo)
    
    def test_initialization(self):
        """Test that engine initializes without starting a game."""
        # Engine should be created but no game started yet
        assert self.engine.get_current_state() is None
    
    def test_start_new_game(self):
        """Test that start_new_game creates initial game state."""
        state = self.engine.start_new_game()
        
        # Verify initial state
        assert isinstance(state, GameState)
        assert state.target_word is not None
        assert len(state.target_word) == 5
        assert state.current_attempt == 0
        assert len(state.attempts) == 0
        assert state.is_won is False
        assert state.is_lost is False
        assert state.is_game_over is False
    
    def test_process_valid_guess(self):
        """Test processing a valid guess increments attempts."""
        state = self.engine.start_new_game()
        target = state.target_word
        
        # Make a guess that's not the target
        # Find a valid word that's not the target
        valid_words = self.word_repo.get_valid_words()
        guess_word = next(w for w in valid_words if w.upper() != target.upper())
        
        new_state = self.engine.process_guess(guess_word)
        
        # Verify state updated
        assert new_state.current_attempt == 1
        assert len(new_state.attempts) == 1
        assert new_state.attempts[0].guess == guess_word.upper()
        assert new_state.is_won is False
        assert new_state.is_lost is False
    
    def test_reject_invalid_word(self):
        """Test that invalid words raise ValueError."""
        self.engine.start_new_game()
        
        # Try to guess a non-existent word
        with pytest.raises(ValueError, match="Invalid word"):
            self.engine.process_guess("XYZQK")
    
    def test_reject_wrong_length(self):
        """Test that wrong-length guesses raise ValueError."""
        self.engine.start_new_game()
        
        # Too short
        with pytest.raises(ValueError, match="must be 5 letters"):
            self.engine.process_guess("CAT")
        
        # Too long
        with pytest.raises(ValueError, match="must be 5 letters"):
            self.engine.process_guess("TESTING")
    
    def test_reject_empty_guess(self):
        """Test that empty guesses raise ValueError."""
        self.engine.start_new_game()
        
        with pytest.raises(ValueError, match="must be 5 letters"):
            self.engine.process_guess("")
    
    def test_win_condition(self):
        """Test that correct guess sets is_won=True."""
        state = self.engine.start_new_game()
        target = state.target_word
        
        # Guess the target word
        new_state = self.engine.process_guess(target)
        
        # Verify win condition
        assert new_state.is_won is True
        assert new_state.is_lost is False
        assert new_state.is_game_over is True
        assert new_state.current_attempt == 1
        assert len(new_state.attempts) == 1
        
        # Verify all letters marked CORRECT
        assert new_state.attempts[0].is_correct is True
        for letter_result in new_state.attempts[0].letters:
            assert letter_result.status == LetterStatus.CORRECT
    
    def test_loss_condition(self):
        """Test that 6 incorrect guesses sets is_lost=True."""
        state = self.engine.start_new_game()
        target = state.target_word
        
        # Find 6 valid words that aren't the target
        valid_words = self.word_repo.get_valid_words()
        wrong_guesses = [
            w for w in valid_words 
            if w.upper() != target.upper()
        ][:6]
        
        # Make 6 wrong guesses
        for i, guess in enumerate(wrong_guesses):
            new_state = self.engine.process_guess(guess)
            
            # Check state after each guess
            if i < 5:
                # Not lost yet
                assert new_state.is_lost is False
                assert new_state.is_game_over is False
            else:
                # Lost after 6th guess
                assert new_state.is_lost is True
                assert new_state.is_won is False
                assert new_state.is_game_over is True
                assert new_state.current_attempt == 6
    
    def test_cannot_guess_after_win(self):
        """Test that guesses after win raise ValueError."""
        state = self.engine.start_new_game()
        target = state.target_word
        
        # Win the game
        self.engine.process_guess(target)
        
        # Try to make another guess
        valid_words = self.word_repo.get_valid_words()
        another_word = valid_words[0]
        
        with pytest.raises(ValueError, match="Game is already over"):
            self.engine.process_guess(another_word)
    
    def test_cannot_guess_after_loss(self):
        """Test that guesses after loss raise ValueError."""
        state = self.engine.start_new_game()
        target = state.target_word
        
        # Make 6 wrong guesses
        valid_words = self.word_repo.get_valid_words()
        wrong_guesses = [w for w in valid_words if w.upper() != target.upper()][:6]
        
        for guess in wrong_guesses:
            self.engine.process_guess(guess)
        
        # Try to make a 7th guess
        with pytest.raises(ValueError, match="Game is already over"):
            self.engine.process_guess(valid_words[6])
    
    def test_case_insensitive_guess(self):
        """Test that guesses are case-insensitive."""
        state = self.engine.start_new_game()
        target = state.target_word
        
        # Process lowercase and uppercase versions
        valid_words = self.word_repo.get_valid_words()
        test_word = next(w for w in valid_words if w.upper() != target.upper())
        
        # Both should work
        state1 = self.engine.process_guess(test_word.lower())
        assert state1.current_attempt == 1
        
        state2 = self.engine.process_guess(test_word.upper())
        assert state2.current_attempt == 2
        
        # Both should be stored as uppercase
        assert state2.attempts[0].guess == test_word.upper()
        assert state2.attempts[1].guess == test_word.upper()
    
    def test_get_current_state(self):
        """Test that get_current_state returns current game state."""
        # No game started yet
        assert self.engine.get_current_state() is None
        
        # Start game
        state1 = self.engine.start_new_game()
        assert self.engine.get_current_state() == state1
        
        # Make a guess
        valid_words = self.word_repo.get_valid_words()
        test_word = valid_words[0]
        state2 = self.engine.process_guess(test_word)
        
        # Current state should be updated
        assert self.engine.get_current_state() == state2
        assert self.engine.get_current_state().current_attempt == 1
    
    def test_reproducible_target_selection(self):
        """Test that seeded engine produces same target."""
        # Create two engines with same seed
        engine1 = GameEngine(InMemoryWordRepository(seed=123))
        engine2 = GameEngine(InMemoryWordRepository(seed=123))
        
        state1 = engine1.start_new_game()
        state2 = engine2.start_new_game()
        
        # Should get same target
        assert state1.target_word == state2.target_word
