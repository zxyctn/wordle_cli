# Wordle CLI

## What This Is

A command-line Wordle game built with Python and Textual UI library. Players guess a 5-letter word within 6 attempts, receiving color-coded feedback (green for correct position, yellow for correct letter but wrong position, gray for letters not in the word). The game features an NYTimes-style grid interface and on-screen QWERTY keyboard.

## Core Value

The game provides accurate, immediate visual feedback that guides players toward the solution through color-coded letter hints in both the grid and keyboard.

## Requirements

### Validated

- ✓ Game validates guesses against words.py dictionary — Phase 1
- ✓ Game selects random target word from dictionary at start — Phase 1
- ✓ Game tracks and displays remaining attempts (6 total) — Phase 1
- ✓ Game prevents invalid (non-dictionary) word submissions — Phase 1
- ✓ Game ends on correct guess or after 6 attempts — Phase 1
- ✓ Duplicate letters correctly evaluated (two-pass algorithm) — Phase 1

### Active

- [ ] Game displays 5x6 grid of cells for letter guesses
- [ ] Cells show visual feedback: green (correct position), yellow (wrong position), gray (not in word)
- [ ] Game enforces 5-letter input limit per guess
- [ ] On-screen QWERTY keyboard reflects same color feedback as grid
- [ ] Keyboard includes backspace and enter keys

### Out of Scope

- Multi-word variants — focus on classic 5-letter format
- Daily puzzle synchronization — standalone game mode only
- Statistics tracking — defer to future version
- Hints or help mode — core gameplay is pure deduction
- Multiplayer or sharing — single-player experience

## Context

The project uses Textual, a modern Python TUI framework for building terminal-based UIs. The words.py file contains a comprehensive word list (game_words array) that serves as both the valid guess dictionary and the pool of possible target words.

The NYTimes Wordle design is well-established: clean grid layout with cells that transform from empty (light gray border) to filled with color-coded feedback. The visual consistency between grid and keyboard helps players track which letters they've tested.

## Constraints

- **Tech Stack**: Python with Textual UI library — required for TUI implementation
- **Architecture**: Ports/Adapters (Hexagonal) pattern — cleanly separate game logic from UI concerns
- **Word List**: Must use existing words.py file — no external word APIs or databases
- **Grid Size**: Fixed 5x6 layout — 5 columns (letters) × 6 rows (attempts)
- **Visual Design**: Match NYTimes Wordle aesthetic — colors, spacing, grid structure

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Textual for UI | Modern Python TUI framework with excellent widget support and styling | — Pending |
| Ports/Adapters architecture | Clean separation enables testing game logic independently of UI, easier to swap UI later | ✓ Good — Phase 1 implemented pure domain layer with zero UI dependencies |
| Use words.py as-is | Pre-existing word list, no need for external dependencies or data sources | ✓ Good — InMemoryWordRepository loads 2,315 words efficiently |
| Two-pass duplicate letter algorithm | Ensures CORRECT positions marked before PRESENT, prevents common Wordle clone bugs | ✓ Good — 9 comprehensive tests verify correct handling |
| Immutable domain models (frozen dataclasses) | Predictable state management, thread-safe by design | ✓ Good — Simplifies testing and prevents mutation bugs |

---
*Last updated: 2026-03-14 after Phase 1*
