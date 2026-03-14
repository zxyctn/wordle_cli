# Architecture Research

**Domain:** Terminal-based word guessing game (Wordle clone)
**Researched:** 2026-03-14
**Confidence:** HIGH

## Standard Architecture

### System Overview (Hexagonal/Ports-Adapters Pattern)

```
┌────────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Textual App (UI Orchestrator)                           │  │
│  │  - Event routing                                         │  │
│  │  - Screen management                                     │  │
│  │  - Reactive attribute updates                            │  │
│  └──────────┬─────────────┬───────────────────────┬─────────┘  │
│             │             │                       │            │
│  ┌──────────▼────┐ ┌──────▼──────┐ ┌─────────────▼─────────┐  │
│  │ Grid Widget   │ │ Keyboard    │ │ Input Widget          │  │
│  │ (6x5 cells)   │ │ (QWERTY)    │ │ (text entry)          │  │
│  └──────────┬────┘ └──────┬──────┘ └─────────────┬─────────┘  │
│             │             │                       │            │
├─────────────┴─────────────┴───────────────────────┴────────────┤
│                        PORT LAYER                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Input Ports (Driving/Primary)                           │  │
│  │  - process_guess(guess: str) -> GuessResult              │  │
│  │  - start_new_game() -> GameState                         │  │
│  │  - get_game_state() -> GameState                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Output Ports (Driven/Secondary)                         │  │
│  │  - WordRepository (validate/select words)                │  │
│  │  - GameStateStore (optional: persistence)                │  │
│  └──────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│                       DOMAIN LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Game Logic (Core Business Rules)                        │  │
│  │  - WordValidator: check if word is valid                 │  │
│  │  - GuessEvaluator: compare guess vs target               │  │
│  │  - GameState: track attempts, results, win/loss          │  │
│  │  - LetterStatus: CORRECT | PRESENT | ABSENT              │  │
│  └──────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Adapters (Driven/Secondary)                             │  │
│  │  - InMemoryWordRepository (reads words.py list)          │  │
│  │  - (Future: FileGameStateStore for persistence)          │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| **WordleApp** | Main application controller, coordinates UI and domain | Textual `App` subclass with reactive attributes |
| **GridWidget** | Displays 6x5 guess grid with color-coded feedback | Custom `Widget` with `compose()` returning 30 `Static` cells |
| **KeyboardWidget** | On-screen QWERTY keyboard with letter feedback | Custom `Widget` composing `Button` widgets for each key |
| **GameEngine** | Core game logic: validate, evaluate, track state | Pure Python class (no Textual dependencies) |
| **GuessEvaluator** | Compares guess against target word, returns letter statuses | Pure function or simple class |
| **WordRepository** | Provides valid words list and selects random target | Interface with in-memory implementation |
| **GameState** | Immutable value object holding current game state | Dataclass or Pydantic model |
| **LetterStatus** | Enum for letter feedback (CORRECT/PRESENT/ABSENT) | Python `Enum` |

## Recommended Project Structure

```
wordle_cli/
├── src/
│   ├── wordle_cli/
│   │   ├── __init__.py
│   │   ├── __main__.py              # Entry point: python -m wordle_cli
│   │   │
│   │   ├── app.py                   # Textual App + screen composition
│   │   │
│   │   ├── domain/                  # Core business logic (no Textual)
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # GameState, GuessResult, LetterStatus
│   │   │   ├── game_engine.py       # GameEngine class (orchestrates rules)
│   │   │   ├── evaluator.py         # GuessEvaluator (compares guess vs target)
│   │   │   └── ports.py             # Abstract interfaces (WordRepository, etc.)
│   │   │
│   │   ├── adapters/                # Infrastructure implementations
│   │   │   ├── __init__.py
│   │   │   └── word_repository.py   # InMemoryWordRepository reads words.py
│   │   │
│   │   ├── widgets/                 # Custom Textual widgets
│   │   │   ├── __init__.py
│   │   │   ├── grid.py              # GuessGridWidget
│   │   │   ├── keyboard.py          # OnScreenKeyboard
│   │   │   └── cell.py              # LetterCell (single grid cell)
│   │   │
│   │   └── styles/                  # CSS files
│   │       └── app.tcss
│   │
│   └── words.py                     # Word list (game_words array)
│
├── tests/
│   ├── test_domain/                 # Test core logic (no UI)
│   │   ├── test_evaluator.py
│   │   └── test_game_engine.py
│   └── test_widgets/                # Test UI components (with Textual Pilot)
│       └── test_grid.py
│
└── pyproject.toml
```

### Structure Rationale

- **`domain/` purity:** Core game logic has zero dependencies on Textual. This enables:
  - Fast unit tests (no UI framework initialization)
  - Easy testing of game rules
  - Potential reuse in web/mobile versions
  
- **`adapters/` for infrastructure:** Implements domain ports (e.g., `WordRepository`). Easy to swap implementations (e.g., API-based word list).

- **`widgets/` for UI components:** Custom Textual widgets compose the interface. Each widget:
  - Extends `Widget` or `Static`
  - Uses reactive attributes for state
  - Responds to domain events via watch methods
  
- **Separation of concerns:** 
  - `app.py` = UI orchestration + wiring domain to widgets
  - `domain/` = game rules
  - `widgets/` = visual representation

## Architectural Patterns

### Pattern 1: Hexagonal Architecture (Ports & Adapters)

**What:** Separates core business logic (domain) from external concerns (UI, data sources) using abstract ports.

**When to use:** Essential for games/apps where:
- Core logic must be testable independently of UI
- Multiple interfaces possible (TUI, GUI, web)
- Clear separation between "what" (domain) and "how" (adapters)

**Trade-offs:**
- **Pros:** Domain logic is pure, testable, reusable; UI can change without breaking rules
- **Cons:** More files/abstractions than needed for trivial apps; requires discipline

**Example:**

```python
# domain/ports.py (abstract interface)
from abc import ABC, abstractmethod

class WordRepository(ABC):
    @abstractmethod
    def get_valid_words(self) -> list[str]:
        """Return list of valid 5-letter words."""
        pass
    
    @abstractmethod
    def get_random_target(self) -> str:
        """Select a random word as the target."""
        pass

# adapters/word_repository.py (concrete implementation)
import random
from words import game_words
from domain.ports import WordRepository

class InMemoryWordRepository(WordRepository):
    def __init__(self):
        self._words = game_words
    
    def get_valid_words(self) -> list[str]:
        return self._words
    
    def get_random_target(self) -> str:
        return random.choice(self._words)

# domain/game_engine.py (uses port, not implementation)
from domain.ports import WordRepository

class GameEngine:
    def __init__(self, word_repo: WordRepository):
        self._word_repo = word_repo
        self._target = word_repo.get_random_target()
    
    def is_valid_guess(self, guess: str) -> bool:
        return guess in self._word_repo.get_valid_words()
```

### Pattern 2: Reactive UI Updates (Textual Reactive Attributes)

**What:** Widgets automatically refresh when reactive attributes change. No manual `refresh()` calls needed.

**When to use:** Always in Textual apps. Simplifies state synchronization between domain and UI.

**Trade-offs:**
- **Pros:** Declarative, reduces boilerplate, automatic consistency
- **Cons:** Can be "magic" for beginners; watch for performance if many reactives

**Example:**

```python
# widgets/grid.py
from textual.reactive import reactive
from textual.widget import Widget
from domain.models import GameState

class GuessGridWidget(Widget):
    game_state: reactive[GameState | None] = reactive(None, recompose=True)
    
    def compose(self):
        # Automatically recomposes when game_state changes
        if self.game_state:
            for attempt in self.game_state.attempts:
                for letter, status in attempt:
                    yield LetterCell(letter, status)
    
# app.py
class WordleApp(App):
    def on_guess_submitted(self, guess: str):
        result = self.game_engine.process_guess(guess)
        # Setting reactive triggers automatic grid update
        self.query_one(GuessGridWidget).game_state = result.new_state
```

### Pattern 3: Message Passing (Textual Events)

**What:** Widgets emit custom messages that bubble up to parent components. Decouples widget implementation from action handling.

**When to use:** For user actions (button clicks, input submission) that trigger domain operations.

**Trade-offs:**
- **Pros:** Loose coupling, composable widgets, testable event handlers
- **Cons:** Indirection can obscure flow for simple cases

**Example:**

```python
# widgets/keyboard.py
from textual.message import Message
from textual.widgets import Button

class OnScreenKeyboard(Widget):
    class LetterPressed(Message):
        """Posted when a letter key is pressed."""
        def __init__(self, letter: str):
            super().__init__()
            self.letter = letter
    
    def on_button_pressed(self, event: Button.Pressed):
        letter = event.button.label
        self.post_message(self.LetterPressed(letter))

# app.py
class WordleApp(App):
    def on_on_screen_keyboard_letter_pressed(self, event: OnScreenKeyboard.LetterPressed):
        self.current_guess += event.letter
        self.update_input_display()
```

## Data Flow

### Request Flow (User Input → Domain → UI Update)

```
[User types letter]
    ↓
[Input Widget captures key event]
    ↓
[Posts InputChanged message]
    ↓
[App handler updates current_guess (reactive)]
    ↓
[Input widget auto-refreshes via watch]

[User presses Enter]
    ↓
[Input Widget posts GuessSubmitted message]
    ↓
[App validates guess with GameEngine]
    ↓
[GameEngine.process_guess() returns GuessResult]
    ↓
[App updates game_state (reactive)]
    ↓
[GridWidget.watch_game_state() recomposes grid]
    ↓
[KeyboardWidget.watch_game_state() updates letter colors]
```

### State Management

```
[GameState (immutable)]
    ↓ (stored as reactive attribute)
[WordleApp.game_state]
    ↓ (watch methods triggered on change)
[GridWidget updates] + [KeyboardWidget updates]
```

### Key Data Flows

1. **Guess Submission Flow:**
   - User input → App validates length → GameEngine validates word → GuessEvaluator compares → GameState updated → Widgets rerender

2. **Visual Feedback Flow:**
   - GameState.attempts contains letter statuses → GridWidget renders cells with colors → KeyboardWidget highlights used letters

3. **Game End Flow:**
   - GameState.is_won or is_lost → App shows modal/screen → Option to restart → New GameEngine instance

## Data Model (Domain Layer)

### Core Models

```python
# domain/models.py
from enum import Enum
from dataclasses import dataclass

class LetterStatus(Enum):
    """Result of evaluating a letter in a guess."""
    CORRECT = "correct"      # Right letter, right position (green)
    PRESENT = "present"      # Right letter, wrong position (yellow)
    ABSENT = "absent"        # Letter not in word (gray)

@dataclass(frozen=True)
class LetterResult:
    """Single letter evaluation."""
    letter: str
    status: LetterStatus
    position: int

@dataclass(frozen=True)
class GuessResult:
    """Result of evaluating a full guess."""
    guess: str
    letters: list[LetterResult]
    is_correct: bool

@dataclass(frozen=True)
class GameState:
    """Immutable snapshot of game state."""
    target_word: str
    attempts: list[GuessResult]  # Max 6
    current_attempt: int
    is_won: bool
    is_lost: bool
    
    @property
    def is_game_over(self) -> bool:
        return self.is_won or self.is_lost
```

### Component Communication

```
GameEngine (domain)
    ↕ (uses)
WordRepository (port) ← implemented by → InMemoryWordRepository (adapter)
    ↕ (uses)
GuessEvaluator (domain)
    ↕ (produces)
GuessResult → GameState
    ↕ (consumed by)
WordleApp (presentation)
    ↕ (renders via)
GridWidget + KeyboardWidget (presentation)
```

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| **MVP (1 player, local)** | Current architecture is perfect. No database, no network. Pure in-memory game. |
| **Daily puzzle sync** | Add `DailyPuzzleRepository` adapter that fetches from API. GameEngine uses same logic. |
| **Statistics tracking** | Add `StatsRepository` port, `FileStatsStore` adapter. GameEngine posts win/loss events. |
| **Multiplayer (local)** | Multiple GameEngine instances, shared UI. Minimal changes to domain layer. |

### Scaling Priorities

1. **First bottleneck:** Word list lookup (17K words)
   - **Fix:** Cache in set for O(1) validation (already efficient in Python)
   
2. **Second bottleneck:** State persistence for statistics
   - **Fix:** Add `StatsRepository` port, implement with SQLite or JSON file

## Anti-Patterns

### Anti-Pattern 1: Putting Game Logic in Widgets

**What people do:**
```python
class GridWidget(Widget):
    def on_input_submitted(self, guess: str):
        # DON'T: game logic in UI code
        if len(guess) != 5:
            return
        correct = [g == t for g, t in zip(guess, self.target)]
        # ... more logic
```

**Why it's wrong:**
- Impossible to test game rules without instantiating UI
- Can't reuse logic for different interfaces
- Violates single responsibility principle

**Do this instead:**
```python
# domain/game_engine.py
class GameEngine:
    def process_guess(self, guess: str) -> GuessResult:
        # Pure game logic, testable without UI
        return self.evaluator.evaluate(guess, self.target)

# widgets/grid.py
class GridWidget(Widget):
    def on_input_submitted(self, guess: str):
        # Delegate to domain, just handle UI update
        result = self.app.game_engine.process_guess(guess)
        self.render_result(result)
```

### Anti-Pattern 2: Direct Coupling to words.py

**What people do:**
```python
# app.py
from words import game_words
class WordleApp(App):
    def validate_guess(self, guess):
        return guess in game_words  # Direct dependency
```

**Why it's wrong:**
- Hard to test with different word lists
- Can't swap data source (API, database, test fixtures)
- Violates dependency inversion principle

**Do this instead:**
```python
# domain/ports.py
class WordRepository(ABC):
    @abstractmethod
    def is_valid_word(self, word: str) -> bool: ...

# app.py
class WordleApp(App):
    def __init__(self, word_repo: WordRepository):
        self.word_repo = word_repo
    
    def validate_guess(self, guess):
        return self.word_repo.is_valid_word(guess)
```

### Anti-Pattern 3: Storing Widget References in Domain

**What people do:**
```python
class GameEngine:
    def __init__(self, grid_widget: GridWidget):
        self.grid = grid_widget  # DON'T: domain knows about UI
    
    def process_guess(self, guess):
        result = self.evaluate(guess)
        self.grid.update(result)  # Domain updates UI directly
```

**Why it's wrong:**
- Domain layer depends on presentation layer (inverted dependency)
- Can't test domain without mocking widgets
- Tight coupling prevents reuse

**Do this instead:**
```python
class GameEngine:
    def process_guess(self, guess) -> GuessResult:
        # Return result, don't update UI
        return self.evaluate(guess)

# app.py
class WordleApp(App):
    def on_input_submitted(self, guess):
        result = self.engine.process_guess(guess)
        # App layer handles UI updates
        self.query_one(GridWidget).display_result(result)
```

## Integration Points

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| **App ↔ GameEngine** | Method calls (process_guess, start_game) | App owns GameEngine instance, calls methods |
| **App ↔ Widgets** | Reactive attributes + Messages | App updates reactives, widgets post messages |
| **GameEngine ↔ WordRepository** | Interface (port) | GameEngine depends on abstract interface |
| **Widgets ↔ Child Widgets** | Compose + reactive props | Parent composes children, passes reactive data |

### Build Order (Dependency Flow)

**Phase 1: Domain Layer (no dependencies)**
1. `domain/models.py` - LetterStatus, GameState, GuessResult
2. `domain/ports.py` - WordRepository interface
3. `domain/evaluator.py` - GuessEvaluator (pure logic)
4. `domain/game_engine.py` - GameEngine (orchestrates)

**Phase 2: Infrastructure Layer (depends on domain)**
5. `adapters/word_repository.py` - InMemoryWordRepository

**Phase 3: Presentation Layer (depends on domain + Textual)**
6. `widgets/cell.py` - LetterCell (single grid cell)
7. `widgets/grid.py` - GuessGridWidget (composes cells)
8. `widgets/keyboard.py` - OnScreenKeyboard
9. `app.py` - WordleApp (wires everything together)

**This build order ensures:**
- Core logic can be built and tested first (TDD-friendly)
- UI can iterate independently without breaking rules
- Clear dependency direction (presentation → domain, never reverse)

## Testing Strategy

### Domain Layer Tests (Fast, No Textual)

```python
# tests/test_domain/test_evaluator.py
def test_all_correct():
    evaluator = GuessEvaluator()
    result = evaluator.evaluate("WORLD", "WORLD")
    assert all(lr.status == LetterStatus.CORRECT for lr in result.letters)

def test_letter_present_wrong_position():
    evaluator = GuessEvaluator()
    result = evaluator.evaluate("DROWN", "WORLD")
    # D is PRESENT (in target but wrong spot)
    assert result.letters[0].status == LetterStatus.PRESENT
```

### Widget Tests (Textual Pilot)

```python
# tests/test_widgets/test_grid.py
from textual.pilot import Pilot
from wordle_cli.widgets.grid import GuessGridWidget

async def test_grid_displays_guess_result():
    async with WordleApp().run_test() as pilot:
        app = pilot.app
        grid = app.query_one(GuessGridWidget)
        
        # Simulate game state update
        grid.game_state = GameState(
            target_word="WORLD",
            attempts=[...],
            current_attempt=1,
            is_won=False,
            is_lost=False
        )
        
        await pilot.pause()
        
        # Assert grid rendered correctly
        cells = grid.query("LetterCell")
        assert len(cells) == 30  # 6 attempts × 5 letters
```

## Sources

**HIGH Confidence:**
- [Textual Official Docs - App Basics](https://textual.textualize.io/guide/app/) - Textual architecture, reactive attributes, widget composition
- [Textual Official Docs - Widgets](https://textual.textualize.io/guide/widgets/) - Custom widgets, event handling, composition patterns
- [Textual Official Docs - Reactivity](https://textual.textualize.io/guide/reactivity/) - Reactive attributes, watch methods, compute methods
- [Wikipedia - Hexagonal Architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) - Ports & adapters pattern, separation of concerns

**MEDIUM Confidence:**
- Hexagonal architecture patterns applied to Python - Standard software engineering practice, not Textual-specific
- Game state management patterns - Common in game development, adapted for TUI context

**Rationale for Wordle CLI:**
- Hexagonal architecture is specified in PROJECT.md constraints
- Textual framework dictates reactive UI patterns
- Word validation requires clear domain/infrastructure boundary (words.py)
- Small scope (single-player, no persistence) keeps architecture simple but extensible

---
*Architecture research for: Wordle CLI with Textual UI and Hexagonal Architecture*
*Researched: 2026-03-14*
