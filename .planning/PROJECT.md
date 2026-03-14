# Wordle CLI

## What This Is

A command-line Wordle game built with Python and Textual UI library. Players guess a 5-letter word within 6 attempts, receiving color-coded feedback (green for correct position, yellow for correct letter but wrong position, gray for letters not in the word). The game features an NYTimes-style grid interface and on-screen QWERTY keyboard.

## Core Value

The game provides accurate, immediate visual feedback that guides players toward the solution through color-coded letter hints in both the grid and keyboard.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Game displays 5x6 grid of cells for letter guesses
- [ ] Cells show visual feedback: green (correct position), yellow (wrong position), gray (not in word)
- [ ] Game validates guesses against words.py dictionary
- [ ] Game selects random target word from dictionary at start
- [ ] Game enforces 5-letter input limit per guess
- [ ] Game tracks and displays remaining attempts (6 total)
- [ ] On-screen QWERTY keyboard reflects same color feedback as grid
- [ ] Keyboard includes backspace and enter keys
- [ ] Game prevents invalid (non-dictionary) word submissions
- [ ] Game ends on correct guess or after 6 attempts

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
| Ports/Adapters architecture | Clean separation enables testing game logic independently of UI, easier to swap UI later | — Pending |
| Use words.py as-is | Pre-existing word list, no need for external dependencies or data sources | — Pending |

---
*Last updated: 2025-03-14 after initialization*
