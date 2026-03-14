"""Grid widget for displaying the Wordle game grid."""

from textual.containers import Grid
from textual.reactive import reactive

from wordle_cli.domain.models import GameState
from .cell import LetterCell


class GuessGridWidget(Grid):
    """A 5×6 grid widget that displays the Wordle game state.
    
    The grid shows:
    - 6 rows representing the 6 allowed guesses
    - 5 columns for the 5 letters in each guess
    - Filled rows show guess results with color-coded feedback
    - Current input row shows letters being typed
    - Empty rows show unfilled cells with gray borders
    
    The widget uses reactive attributes that trigger recomposition
    when the state changes, automatically updating the grid display.
    """

    game_state: reactive[GameState | None] = reactive(None)
    current_input: reactive[str] = reactive("")
    
    def __init__(self, **kwargs):
        """Initialize the grid with explicit size."""
        super().__init__(**kwargs)
        self.styles.grid_size_columns = 5
        self.styles.grid_size_rows = 6
        self._cells = []

    def compose(self):
        """Compose the 5×6 grid of letter cells.
        
        Yields LetterCell widgets for all 30 positions (6 rows × 5 columns).
        Cells start empty and are updated via watch methods.
        """
        # Create all 30 cells empty initially
        for _ in range(30):
            cell = LetterCell("", None)
            self._cells.append(cell)
            yield cell
    
    def watch_game_state(self, new_state: GameState | None) -> None:
        """Update cells when game state changes."""
        if not self._cells:
            return
        
        self._update_cells()
    
    def watch_current_input(self, new_input: str) -> None:
        """Update cells when current input changes."""
        if not self._cells:
            return
        
        self._update_cells()
    
    def _update_cells(self) -> None:
        """Update all cells based on current game state and input."""
        if not self.game_state:
            return
        
        cell_index = 0
        num_completed = len(self.game_state.attempts)
        
        # Update cells for completed attempts
        for attempt in self.game_state.attempts:
            for letter_result in attempt.letters:
                if cell_index < 30:
                    cell = self._cells[cell_index]
                    cell.update(letter_result.letter.upper())
                    cell.set_letter_status(letter_result.status)
                    cell_index += 1
        
        # Update cells for current input row (if game is not over and < 6 attempts)
        if not self.game_state.is_game_over and num_completed < 6:
            padded = self.current_input.ljust(5)
            for char in padded:
                if cell_index < 30:
                    letter = char.upper() if char.strip() else " "
                    cell = self._cells[cell_index]
                    cell.update(letter)
                    cell.set_letter_status(None)
                    cell_index += 1
        
        # Update remaining cells to be empty
        while cell_index < 30:
            cell = self._cells[cell_index]
            cell.update(" ")
            cell.set_letter_status(None)
            cell_index += 1
