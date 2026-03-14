"""Letter cell widget for displaying individual letters with status colors."""

from textual.widgets import Static

from wordle_cli.domain.models import LetterStatus


class LetterCell(Static):
    """A single letter cell that displays a letter with color-coded status.
    
    The cell shows:
    - Empty state (letter="", status=None): Light gray border, no background
    - CORRECT: Green background (#6aaa64) - letter is in correct position
    - PRESENT: Yellow background (#c9b458) - letter is in word but wrong position
    - ABSENT: Gray background (#787c7e) - letter is not in the word
    """

    def __init__(self, letter: str = "", status: LetterStatus | None = None) -> None:
        """Initialize a letter cell.
        
        Args:
            letter: The letter to display (will be uppercased). Empty string for empty cell.
            status: The letter status determining the color. None for empty cell.
        """
        # Display letter in uppercase, or space for empty cells
        display_text = letter.upper() if letter else " "
        super().__init__(display_text, classes="letter-cell")
        
        # Store the status to apply after mount
        self._status = status
    
    def on_mount(self) -> None:
        """Apply initial styles after widget is mounted."""
        self.set_letter_status(self._status)
    
    def set_letter_status(self, status: LetterStatus | None) -> None:
        """Set the styling based on letter status using inline styles."""
        self._status = status
        
        # Remove all CSS classes first
        self.remove_class("cell-empty", "cell-correct", "cell-present", "cell-absent")
        
        # Add the appropriate CSS class based on status value (not enum comparison)
        # Using .value to avoid enum identity issues when module is imported differently
        if status is None:
            self.add_class("cell-empty")
        elif hasattr(status, 'value'):
            # Use string value comparison to avoid enum identity issues
            if status.value == "correct":
                self.add_class("cell-correct")
            elif status.value == "present":
                self.add_class("cell-present")
            elif status.value == "absent":
                self.add_class("cell-absent")
        
        # Force a refresh to ensure styles are applied
        self.refresh()
