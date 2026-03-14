"""Main Textual application for Wordle CLI."""

from textual.app import App, ComposeResult
from textual.containers import Vertical, Center
from textual.widgets import Button, Static, Footer

from wordle_cli.adapters.word_repository import InMemoryWordRepository
from wordle_cli.domain.game_engine import GameEngine
from wordle_cli.widgets import GuessGridWidget, KeyboardWidget


class WordleApp(App):
    """A Wordle game built with Textual.
    
    Controls:
    - Type letters A-Z to enter guess
    - Backspace to delete last letter
    - Enter to submit guess
    - Q or Ctrl+C to quit
    """

    CSS_PATH = "styles/app.tcss"
    TITLE = "Wordle CLI"
    
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+r", "restart", "New Game"),
    ]

    def __init__(self):
        """Initialize the app."""
        super().__init__()
        self.word_repo = InMemoryWordRepository()
        self.engine = GameEngine(self.word_repo)
        self.current_input = ""

    def compose(self) -> ComposeResult:
        """Compose the app widgets."""
        with Center():
            yield GuessGridWidget(id="grid")
        with Center():
            yield KeyboardWidget(id="keyboard")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize game engine and start new game."""
        self.engine.start_new_game()
        self._update_display()

    def on_key(self, event) -> None:
        """Handle keyboard input."""
        key = event.key
        
        # Ignore input if game is over
        state = self.engine.get_current_state()
        if state.is_won or state.is_lost:
            return
        
        # Handle letter keys (a-z)
        if key.isalpha() and len(key) == 1:
            if len(self.current_input) < 5:
                self.current_input += key.upper()
                self._update_input_display()
        
        # Handle backspace
        elif key == "backspace":
            if self.current_input:
                self.current_input = self.current_input[:-1]
                self._update_input_display()
        
        # Handle enter
        elif key == "enter":
            self._submit_guess()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle on-screen keyboard button presses."""
        key = event.button.name
        
        # Ignore if game is over
        state = self.engine.get_current_state()
        if state and (state.is_won or state.is_lost):
            return
        
        if key == "ENTER":
            self._submit_guess()
        elif key == "⌫":
            if self.current_input:
                self.current_input = self.current_input[:-1]
                self._update_input_display()
        elif len(self.current_input) < 5:
            self.current_input += key
            self._update_input_display()
    
    def action_restart(self) -> None:
        """Action handler for Ctrl+R to restart the game."""
        self._restart_game()

    def _submit_guess(self) -> None:
        """Submit the current input as a guess."""
        if len(self.current_input) != 5:
            self.notify("Not enough letters!", severity="warning", timeout=2)
            return
        
        guess = self.current_input
        
        try:
            result = self.engine.process_guess(guess)
        except ValueError as e:
            error_msg = str(e)
            if "Invalid word" in error_msg:
                self.notify("Not in word list!", severity="warning", timeout=2)
            else:
                self.notify(str(e), severity="error", timeout=2)
            return
        
        # Clear input and update display
        self.current_input = ""
        self._update_display()
        
        # Check for win/loss
        state = self.engine.get_current_state()
        if state.is_won:
            self.notify("[bold green]🎉 You won![/bold green]", severity="information", timeout=None)
        elif state.is_lost:
            self.notify(f"Game over! The word was {state.target_word}", severity="error", timeout=None)

    def _update_display(self) -> None:
        """Update all widgets with current game state."""
        state = self.engine.get_current_state()
        
        # Update grid with state and current input
        grid = self.query_one("#grid", GuessGridWidget)
        grid.game_state = state
        grid.current_input = self.current_input
        
        # Update keyboard
        keyboard = self.query_one("#keyboard", KeyboardWidget)
        keyboard.game_state = state

    def _update_input_display(self) -> None:
        """Update the grid with current input."""
        grid = self.query_one("#grid", GuessGridWidget)
        grid.current_input = self.current_input
    
    def _restart_game(self) -> None:
        """Restart the game with a new word."""
        self.engine.start_new_game()
        self.current_input = ""
        self._update_display()
        self.notify("New game started!", severity="information", timeout=2)
