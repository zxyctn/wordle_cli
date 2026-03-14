"""Input row widget for displaying the current guess being typed."""

from textual.reactive import reactive
from textual.widget import Widget

from .cell import LetterCell


class InputRowWidget(Widget):
    """A row widget that shows the current input buffer (0-5 letters).
    
    Displays letters as they're typed in empty cells. This provides
    real-time visual feedback before the guess is submitted.
    """

    current_input: reactive[str] = reactive("", recompose=True)

    def compose(self):
        """Compose 5 cells showing current input + empty cells."""
        # Pad input to 5 characters
        padded = self.current_input.ljust(5)
        
        for char in padded:
            letter = char if char.strip() else ""
            yield LetterCell(letter, None)
