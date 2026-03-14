"""On-screen keyboard widget with letter status feedback."""

from textual.containers import Horizontal, Vertical, Center
from textual.reactive import reactive
from textual.widgets import Button

from wordle_cli.domain.models import GameState, LetterStatus


class KeyboardWidget(Vertical):
    """QWERTY keyboard with color-coded feedback.
    
    Layout:
    Row 1: Q W E R T Y U I O P
    Row 2: A S D F G H J K L
    Row 3: ENTER Z X C V B N M ⌫
    
    Keys update colors to match grid feedback (gray/yellow/green)
    after each guess submission.
    """
    
    game_state: reactive[GameState | None] = reactive(None, recompose=True)
    
    # Keyboard layout rows
    ROWS = [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["ENTER", "Z", "X", "C", "V", "B", "N", "M", "⌫"],
    ]
    
    def compose(self):
        """Compose keyboard rows with status-aware buttons."""
        # Calculate letter statuses from game state
        letter_statuses = self._calculate_letter_statuses()
        
        for row in self.ROWS:
            with Center():
                with Horizontal(classes="keyboard-row"):
                    for key in row:
                        # Determine button class based on letter status
                        if key in ("ENTER", "⌫"):
                            classes = "key key-special"
                        else:
                            status = letter_statuses.get(key)
                            if status and status.value == "correct":
                                classes = "key key-correct"
                            elif status and status.value == "present":
                                classes = "key key-present"
                            elif status and status.value == "absent":
                                classes = "key key-absent"
                            else:
                                classes = "key key-unused"
                        
                        button = Button(key, classes=classes, name=key)
                        button.can_focus = False  # Prevent focus stealing from keyboard input
                        yield button
    
    def _calculate_letter_statuses(self) -> dict[str, LetterStatus]:
        """Calculate the best status for each letter based on all attempts.
        
        Priority: CORRECT > PRESENT > ABSENT
        Once a letter has a status, it can only upgrade, never downgrade.
        """
        if not self.game_state:
            return {}
        
        statuses: dict[str, LetterStatus] = {}
        
        for attempt in self.game_state.attempts:
            for letter_result in attempt.letters:
                letter = letter_result.letter.upper()
                current_status = statuses.get(letter)
                new_status = letter_result.status
                
                # Update only if new status has higher priority
                if current_status is None:
                    # First time seeing this letter
                    statuses[letter] = new_status
                elif current_status.value == "absent":
                    # Absent can upgrade to present or correct
                    if new_status.value in ("present", "correct"):
                        statuses[letter] = new_status
                elif current_status.value == "present":
                    # Present can only upgrade to correct
                    if new_status.value == "correct":
                        statuses[letter] = new_status
                # If current is "correct", never change it
        
        return statuses
