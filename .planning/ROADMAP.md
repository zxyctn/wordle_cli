# Roadmap: Wordle CLI

## Overview

This roadmap delivers a terminal-based Wordle game through three focused phases. Starting with pure game logic and word validation, we then build the visual grid with color-coded feedback, and finally add player input controls with the on-screen keyboard. The architecture follows hexagonal (ports & adapters) pattern, keeping domain logic pure and testable before introducing UI complexity. Each phase delivers a verifiable capability that enables the next.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Core Domain & Game Engine** - Pure game logic with word validation and duplicate letter handling (completed 2026-03-14)
- [ ] **Phase 2: Visual Grid & Feedback** - 5x6 grid display with color-coded letter feedback
- [ ] **Phase 3: Input & Keyboard Interface** - Player input controls and on-screen keyboard with feedback

## Phase Details

### Phase 1: Core Domain & Game Engine
**Goal**: Establish testable game rules engine that validates words, evaluates guesses, and tracks game state
**Depends on**: Nothing (first phase)
**Requirements**: GAME-01, GAME-05, GAME-06, GAME-07, GAME-08, LOGIC-01, LOGIC-02, LOGIC-03, LOGIC-04
**Success Criteria** (what must be TRUE):
  1. Game selects a random 5-letter target word from the word list at start
  2. Game correctly validates whether a 5-letter guess exists in the dictionary
  3. Game correctly evaluates duplicate letters in both guesses and target words
  4. Game tracks remaining attempts and detects win (correct guess) or loss (6 failed attempts)
  5. All game logic functions without any UI framework dependencies
**Plans**: TBD

Plans:
- [ ] TBD

### Phase 2: Visual Grid & Feedback
**Goal**: Display game state in NYTimes-style 5x6 grid with immediate color-coded feedback
**Depends on**: Phase 1
**Requirements**: GAME-02, VIS-01, VIS-02, VIS-03, VIS-04, VIS-05, VIS-06
**Success Criteria** (what must be TRUE):
  1. Player sees a 5x6 grid of cells displaying their guess history
  2. Empty cells show light gray borders before being filled
  3. Submitted guess cells immediately show green (correct position), yellow (wrong position), or gray (not in word) backgrounds
  4. Visual design matches NYTimes Wordle aesthetic with proper colors, spacing, and grid structure
**Plans**: TBD

Plans:
- [ ] TBD

### Phase 3: Input & Keyboard Interface
**Goal**: Enable player input with visual keyboard that reflects tested letters
**Depends on**: Phase 2
**Requirements**: GAME-03, GAME-04, KEY-01, KEY-02, KEY-03, KEY-04, KEY-05
**Success Criteria** (what must be TRUE):
  1. Player can type letters to build a 5-letter guess (constrained to 5 characters max)
  2. Player can use backspace to delete letters and enter to submit guesses
  3. On-screen QWERTY keyboard displays all letter keys plus backspace and enter
  4. Keyboard keys change color to match grid feedback (gray/yellow/green) after each guess
  5. Player experiences complete guess-submit-feedback loop from input to visual result
**Plans**: TBD

Plans:
- [ ] TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Domain & Game Engine | 0/3 | Complete    | 2026-03-14 |
| 2. Visual Grid & Feedback | 0/TBD | Not started | - |
| 3. Input & Keyboard Interface | 0/TBD | Not started | - |
