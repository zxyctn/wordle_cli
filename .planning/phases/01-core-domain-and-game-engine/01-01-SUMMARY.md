---
phase: 01-core-domain-and-game-engine
plan: 01
subsystem: domain
tags: [foundation, domain-models, ports, hexagonal-architecture]
dependencies:
  requires: []
  provides:
    - LetterStatus enum
    - LetterResult, GuessResult, GameState dataclasses
    - WordRepository port interface
  affects: []
tech_stack:
  added:
    - Python dataclasses (frozen=True for immutability)
    - Python enum.Enum
    - Python abc.ABC for port interfaces
  patterns:
    - Hexagonal architecture (ports)
    - Immutable domain models
    - Dependency inversion principle
key_files:
  created:
    - src/wordle_cli/__init__.py
    - src/wordle_cli/domain/__init__.py
    - src/wordle_cli/domain/models.py
    - src/wordle_cli/domain/ports.py
  modified: []
decisions:
  - Used frozen dataclasses for immutability ensuring predictable state management
  - String enum values for LetterStatus to enable easy serialization
  - Validation in GameState.__post_init__ to enforce current_attempt consistency
  - Modern Python type hints (list[str] instead of List[str])
metrics:
  duration: 1
  completed: 2026-03-14T09:43:13Z
  tasks_completed: 2
  files_created: 4
  lines_added: 121
---

# Phase 01 Plan 01: Domain Models & Port Interfaces Summary

**One-liner:** Immutable domain models (GameState, GuessResult, LetterResult) with LetterStatus enum and WordRepository port interface using frozen dataclasses and ABC pattern.

## Overview

Established the foundational domain layer with pure Python types representing game state, letter evaluation results, and abstract interfaces for external dependencies. All models are immutable (frozen dataclasses) for predictable state management and thread safety.

## Tasks Completed

| Task | Name                          | Status | Commit  |
| ---- | ----------------------------- | ------ | ------- |
| 1    | Create domain models module   | ✅     | b4e57ac |
| 2    | Create port interfaces        | ✅     | fa40d37 |

### Task 1: Create domain models module

**Status:** ✅ Complete

**Files created:**
- `src/wordle_cli/__init__.py` - Package root
- `src/wordle_cli/domain/__init__.py` - Domain exports
- `src/wordle_cli/domain/models.py` - Core domain models

**Implementation:**
- `LetterStatus` enum with CORRECT ("correct"), PRESENT ("present"), ABSENT ("absent") values
- `LetterResult` frozen dataclass: letter, status, position (0-4)
- `GuessResult` frozen dataclass: guess, letters list, is_correct boolean
- `GameState` frozen dataclass: target_word, attempts list (max 6), current_attempt (0-6), is_won, is_lost
- `GameState.is_game_over` property returns True if won or lost
- Validation in `__post_init__` ensures current_attempt matches len(attempts)

**Commit:** b4e57ac

### Task 2: Create port interfaces

**Status:** ✅ Complete

**Files created:**
- `src/wordle_cli/domain/ports.py` - Abstract interfaces

**Implementation:**
- `WordRepository` ABC with three abstract methods:
  - `get_valid_words() -> list[str]` - Returns all valid 5-letter words
  - `is_valid_word(word: str) -> bool` - Validates word exists in dictionary
  - `get_random_target() -> str` - Selects random target word
- Detailed docstrings explaining each method's contract
- Exported from domain package

**Commit:** fa40d37

## Deviations from Plan

None - plan executed exactly as written.

## Technical Decisions

1. **Frozen dataclasses for immutability**
   - Used `@dataclass(frozen=True)` for all domain models
   - Ensures thread safety and predictable state management
   - Prevents accidental mutations that could cause bugs

2. **String enum values**
   - LetterStatus uses string values ("correct", "present", "absent")
   - Enables easy JSON serialization for potential future features
   - More readable in debugging output

3. **Validation in __post_init__**
   - GameState validates current_attempt matches len(attempts)
   - Catches state inconsistencies at construction time
   - Prevents invalid game states from being created

4. **Modern type hints**
   - Used `list[str]` instead of `typing.List[str]` (Python 3.9+)
   - Cleaner syntax, aligned with modern Python practices

## Verification Results

All verification checks passed:

✓ Files created in correct directory structure (src/wordle_cli/domain/)
✓ Models are immutable (frozen dataclasses)
✓ LetterStatus enum has correct values (correct/present/absent)
✓ GameState has is_game_over computed property
✓ WordRepository is abstract with 3 required methods
✓ No external dependencies (only Python stdlib)
✓ All types properly exported from domain/__init__.py

## Output Artifacts

### Domain Models (src/wordle_cli/domain/models.py)

**Exports:** LetterStatus, LetterResult, GuessResult, GameState
**Lines:** 82
**Purpose:** Pure domain models with zero external dependencies

### Port Interfaces (src/wordle_cli/domain/ports.py)

**Exports:** WordRepository
**Lines:** 45
**Purpose:** Abstract interfaces for dependency inversion

### Package Exports (src/wordle_cli/domain/__init__.py)

**Exports:** All domain types
**Lines:** 11
**Purpose:** Clean public API for domain layer

## Dependencies

**Requires:** None (foundation layer)

**Provides:**
- Domain models for game state representation
- Port interface for word repository implementations
- Foundation for game engine logic

**Affects:** All future layers depend on these models

## Next Steps

The domain layer foundation is complete. Next plans should:
1. Implement game engine logic using these models
2. Create adapters implementing WordRepository port
3. Build UI components that display game state

## Self-Check

Verifying all claimed outputs exist...

```bash
# Check files exist
✓ FOUND: src/wordle_cli/__init__.py
✓ FOUND: src/wordle_cli/domain/__init__.py
✓ FOUND: src/wordle_cli/domain/models.py
✓ FOUND: src/wordle_cli/domain/ports.py

# Check commits exist
✓ FOUND: b4e57ac (feat(01-01): create domain models module)
✓ FOUND: fa40d37 (feat(01-01): create port interfaces)
```

## Self-Check: PASSED

All files created and commits recorded successfully.
