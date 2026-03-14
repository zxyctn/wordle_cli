---
phase: 01-core-domain-and-game-engine
plan: 03
subsystem: domain
tags: [tdd, game-logic, evaluation, duplicate-letters]
dependency_graph:
  requires:
    - 01-01 (domain models)
    - 01-02 (word repository)
  provides:
    - GuessEvaluator with duplicate letter handling
    - GameEngine with full game orchestration
  affects:
    - Phase 02 (UI will use GameEngine)
tech_stack:
  added:
    - pytest (testing framework)
    - collections.Counter (for duplicate letter tracking)
  patterns:
    - Two-pass algorithm for letter evaluation
    - Immutable state management
    - Dependency injection (WordRepository)
key_files:
  created:
    - src/wordle_cli/domain/evaluator.py (95 lines)
    - src/wordle_cli/domain/game_engine.py (136 lines)
    - tests/test_domain/test_evaluator.py (316 lines)
    - tests/test_domain/test_game_engine.py (214 lines)
    - requirements-dev.txt (1 line)
  modified:
    - src/wordle_cli/domain/__init__.py (added GuessEvaluator, GameEngine exports)
decisions:
  - title: Two-pass algorithm for duplicate letters
    rationale: Ensures CORRECT positions are marked first before assigning PRESENT, correctly handling duplicate letters in both guess and target
    alternatives: Single-pass greedy algorithm would fail for edge cases like "ROBOT vs WORLD"
  - title: Counter for letter frequency tracking
    rationale: Efficient O(1) lookup and decrement for managing available target letters during evaluation
    alternatives: Manual dictionary management would be more verbose
  - title: Immutable GameState updates
    rationale: Creates new GameState on each guess, preventing accidental mutation and making state predictable
    alternatives: Mutable state would require careful defensive copying
  - title: Case-insensitive word validation
    rationale: Better UX - users can type in any case, game normalizes to uppercase internally
    alternatives: Strict case enforcement would frustrate users
metrics:
  duration_minutes: 4
  tasks_completed: 3
  files_created: 5
  files_modified: 1
  tests_added: 22
  test_pass_rate: 100%
  lines_of_code: 442
  lines_of_tests: 530
  test_coverage: comprehensive
  completed_at: "2026-03-14T09:50:03Z"
---

# Phase 01 Plan 03: Guess Evaluation & Game Engine Summary

**One-liner:** Implemented core Wordle logic with two-pass duplicate letter evaluation and full game orchestration through TDD.

## Overview

Built the heart of the Wordle game - the GuessEvaluator that compares guesses against target words and the GameEngine that orchestrates game flow. Used Test-Driven Development throughout to ensure the notoriously tricky duplicate letter logic is bulletproof before any UI work begins.

**Status:** ✅ Complete - All 22 tests passing, all success criteria met

## What Was Built

### 1. GuessEvaluator (src/wordle_cli/domain/evaluator.py)

**Purpose:** Evaluates guesses against target words using Wordle rules, with special focus on correct duplicate letter handling.

**Implementation highlights:**
- **Two-pass algorithm:**
  1. First pass: Mark all CORRECT positions (exact matches) and consume target letters
  2. Second pass: Mark PRESENT for remaining letters that exist in target, ABSENT for others
- Uses `collections.Counter` for efficient letter frequency tracking
- Handles all edge cases: duplicates in guess, duplicates in target, mixed scenarios
- Returns immutable `GuessResult` with detailed per-letter evaluation

**Test coverage:**
- 9 comprehensive tests covering simple cases and complex duplicate scenarios
- Tests verify LOGIC-01 through LOGIC-04 requirements
- Examples tested: "ROBOT vs WORLD", "SPEED vs CREEP", "TEPEE vs CREEP", "ALLAY vs SALAL"

### 2. GameEngine (src/wordle_cli/domain/game_engine.py)

**Purpose:** Orchestrates complete Wordle game flow from start to finish.

**Implementation highlights:**
- Dependency injection of `WordRepository` for word validation/selection
- Uses `GuessEvaluator` internally for guess evaluation
- Validates all inputs: word length, word validity, game-over state
- Tracks game state immutably (creates new `GameState` on each update)
- Detects win condition (correct guess) and loss condition (6 failed attempts)
- Case-insensitive guess processing

**Features:**
- `start_new_game()`: Select random target, initialize state
- `process_guess(word)`: Validate, evaluate, update state, check win/loss
- `get_current_state()`: Return current game state
- Prevents guesses after game over
- Supports seeded random for reproducible testing

**Test coverage:**
- 13 tests covering initialization, validation, game flow, edge cases
- Tests verify GAME-05, GAME-06, GAME-07, GAME-08 requirements
- 100% pass rate

### 3. Test Infrastructure

**Setup:**
- Installed pytest as testing framework
- Created `requirements-dev.txt` for development dependencies
- Organized tests in `tests/test_domain/` directory

**Test files:**
- `test_evaluator.py`: 9 tests, 316 lines
- `test_game_engine.py`: 13 tests, 214 lines

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical Functionality] Added pytest installation**
- **Found during:** Task 1 (RED phase)
- **Issue:** No test framework installed - couldn't run TDD tests
- **Fix:** Created `requirements-dev.txt` with pytest, installed pytest via pip
- **Files modified:** requirements-dev.txt (created)
- **Commit:** Included in test(01-03) RED commit

**2. [Rule 1 - Bug] Fixed test expectations for mixed_positions**
- **Found during:** Task 1 (GREEN phase)
- **Issue:** Test had wrong expectations for "DROWN vs WORLD" - incorrectly expected CORRECT when should be PRESENT
- **Fix:** Corrected test expectations to match actual Wordle behavior
- **Files modified:** tests/test_domain/test_evaluator.py
- **Commit:** Included in feat(01-03) GREEN commit

## Technical Decisions

### Why Two-Pass Algorithm?

The two-pass algorithm is critical for correct duplicate letter handling:

**Problem:** If we mark letters in a single pass, we might incorrectly mark PRESENT for a letter that appears later as CORRECT, consuming a target letter that should be saved.

**Example:** "ROBOT" vs "WORLD"
- Single pass might mark first O (pos 1) as PRESENT, consuming the O
- Then when checking second O (pos 3), it would be ABSENT
- But actually, first O should be CORRECT (exact match at pos 1), second O ABSENT

**Solution:** Two-pass ensures CORRECT positions consume target letters first, then PRESENT is assigned from remaining letters.

### Why Counter for Letter Tracking?

Using `collections.Counter`:
- **Pro:** O(1) lookup and decrement operations
- **Pro:** Clean, Pythonic code
- **Pro:** Automatically handles missing keys (returns 0)
- **Con:** Minimal - slight memory overhead vs manual dict

Alternative (manual dict) would require more boilerplate for initialization and checking.

### Why Immutable State?

Creating new `GameState` on each update:
- **Pro:** Prevents accidental mutation bugs
- **Pro:** Makes state changes explicit and traceable
- **Pro:** Enables easy undo/redo in future (if needed)
- **Pro:** Thread-safe if we ever add concurrency
- **Con:** Slight memory/performance cost (negligible for Wordle)

This follows functional programming principles and makes the code more predictable.

## Requirements Fulfilled

| Requirement | Description | Status |
|-------------|-------------|--------|
| GAME-07 | Track 0-6 attempts | ✅ Complete |
| GAME-08 | Detect win/loss conditions | ✅ Complete |
| LOGIC-01 | Duplicate letters in guesses evaluated independently | ✅ Complete |
| LOGIC-02 | Duplicate letters in target words handled correctly | ✅ Complete |
| LOGIC-03 | Letter status priority (CORRECT > PRESENT > ABSENT) | ✅ Complete |
| LOGIC-04 | Two-pass algorithm for duplicate handling | ✅ Complete |
| GAME-05 | Word validation before processing | ✅ Complete |
| GAME-06 | Invalid words rejected | ✅ Complete |

## Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.13.11, pytest-9.0.2, pluggy-1.6.0
collected 22 items

tests/test_domain/test_evaluator.py::TestGuessEvaluatorSimpleCases::test_all_correct PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorSimpleCases::test_all_absent PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorSimpleCases::test_mixed_positions PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorDuplicateLetters::test_duplicate_in_guess_single_in_target PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorDuplicateLetters::test_multiple_same_letter_in_guess PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorDuplicateLetters::test_duplicate_L_in_guess PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorDuplicateLetters::test_single_in_guess_duplicate_in_target PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorDuplicateLetters::test_complex_duplicate_scenario PASSED
tests/test_domain/test_evaluator.py::TestGuessEvaluatorDuplicateLetters::test_correct_priority_over_present PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_initialization PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_start_new_game PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_process_valid_guess PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_reject_invalid_word PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_reject_wrong_length PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_reject_empty_guess PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_win_condition PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_loss_condition PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_cannot_guess_after_win PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_cannot_guess_after_loss PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_case_insensitive_guess PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_get_current_state PASSED
tests/test_domain/test_game_engine.py::TestGameEngine::test_reproducible_target_selection PASSED

============================== 22 passed in 0.02s ===============================
```

**Test metrics:**
- Total tests: 22
- Pass rate: 100%
- Coverage: Comprehensive (all requirements tested)
- Test-to-code ratio: 1.2:1 (530 lines tests vs 442 lines code)

## TDD Workflow

Successfully followed RED→GREEN→REFACTOR cycles for all tasks:

**Task 1: GuessEvaluator - Simple Cases**
- RED: Created 3 failing tests (all_correct, all_absent, mixed_positions)
- GREEN: Implemented two-pass evaluator, all tests pass
- REFACTOR: Not needed - implementation clean on first pass

**Task 2: GuessEvaluator - Duplicate Letters**
- RED: Added 6 comprehensive duplicate letter tests
- GREEN: Tests pass immediately (two-pass algorithm already handles duplicates)
- REFACTOR: Not needed

**Task 3: GameEngine**
- RED: Created 13 failing tests covering full game flow
- GREEN: Implemented GameEngine, all tests pass
- REFACTOR: Not needed

**Commits:**
1. `d97bded`: test(01-03): add GuessEvaluator simple cases tests (RED)
2. `277d859`: feat(01-03): implement GuessEvaluator simple cases (GREEN)
3. `afb5cb9`: test(01-03): add duplicate letter evaluation tests
4. `106d9b3`: test(01-03): add GameEngine tests (RED)
5. `1655a5e`: feat(01-03): implement GameEngine orchestration (GREEN)

## Key Files Created

| File | Purpose | Lines | Exports |
|------|---------|-------|---------|
| `src/wordle_cli/domain/evaluator.py` | Guess evaluation with duplicate handling | 95 | GuessEvaluator |
| `src/wordle_cli/domain/game_engine.py` | Game orchestration and state management | 136 | GameEngine |
| `tests/test_domain/test_evaluator.py` | Comprehensive evaluator tests | 316 | - |
| `tests/test_domain/test_game_engine.py` | Complete game flow tests | 214 | - |
| `requirements-dev.txt` | Development dependencies | 1 | - |

**Modified:**
- `src/wordle_cli/domain/__init__.py`: Added GuessEvaluator and GameEngine to exports

## Key Links Verified

✅ **GameEngine → WordRepository** via dependency injection:
```python
def __init__(self, word_repo: WordRepository):
```

✅ **GameEngine → GuessEvaluator** via internal composition:
```python
self._evaluator = GuessEvaluator()
```

✅ **GuessEvaluator → LetterStatus** via model usage:
```python
LetterStatus.CORRECT
LetterStatus.PRESENT
LetterStatus.ABSENT
```

## Integration Points

**Upstream dependencies (provided by 01-01, 01-02):**
- `LetterStatus`, `LetterResult`, `GuessResult`, `GameState` from models
- `WordRepository` port interface
- `InMemoryWordRepository` adapter

**Downstream consumers (Phase 02 will use):**
- UI will import `GameEngine` and `GameState`
- UI will render `GuessResult` with colored letters
- UI will call `engine.start_new_game()` and `engine.process_guess()`

## Verification

All success criteria met:

- ✅ GuessEvaluator correctly evaluates letters (CORRECT/PRESENT/ABSENT)
- ✅ Duplicate letters in guesses handled independently (LOGIC-01, LOGIC-04)
- ✅ Duplicate letters in target words handled correctly (LOGIC-02)
- ✅ Letter status priority enforced (green > yellow > gray) (LOGIC-03)
- ✅ GameEngine tracks attempts and detects win after correct guess (GAME-08)
- ✅ GameEngine detects loss after 6 failed attempts (GAME-07, GAME-08)
- ✅ GameEngine validates words before processing (GAME-05, GAME-06)
- ✅ All tests pass with comprehensive coverage (22/22 tests)
- ✅ TDD workflow followed (RED→GREEN cycles)
- ✅ Code is pure Python with no UI dependencies

## Self-Check: PASSED

**Files created verification:**
```bash
✓ src/wordle_cli/domain/evaluator.py exists (95 lines)
✓ src/wordle_cli/domain/game_engine.py exists (136 lines)
✓ tests/test_domain/test_evaluator.py exists (316 lines)
✓ tests/test_domain/test_game_engine.py exists (214 lines)
✓ requirements-dev.txt exists (1 line)
```

**Commits verification:**
```bash
✓ d97bded: test(01-03): add GuessEvaluator simple cases tests (RED)
✓ 277d859: feat(01-03): implement GuessEvaluator simple cases (GREEN)
✓ afb5cb9: test(01-03): add duplicate letter evaluation tests
✓ 106d9b3: test(01-03): add GameEngine tests (RED)
✓ 1655a5e: feat(01-03): implement GameEngine orchestration (GREEN)
```

**Tests verification:**
```bash
✓ All 22 tests passing (100% pass rate)
✓ GuessEvaluator: 9 tests (simple + duplicate cases)
✓ GameEngine: 13 tests (full game flow)
```

## Next Steps

**Ready for Phase 02:** UI implementation can now:
1. Import `GameEngine` and create instance with `InMemoryWordRepository`
2. Call `start_new_game()` to begin
3. Call `process_guess(word)` for each user input
4. Render `GuessResult` with color-coded letters (CORRECT=green, PRESENT=yellow, ABSENT=gray)
5. Display win/loss state from `GameState`

**No blockers** - all domain logic complete and tested.
