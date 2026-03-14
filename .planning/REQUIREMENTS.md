# Requirements: Wordle CLI

**Defined:** 2025-03-14
**Core Value:** The game provides accurate, immediate visual feedback that guides players toward the solution through color-coded letter hints in both the grid and keyboard.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Core Gameplay

- [x] **GAME-01**: Game selects random 5-letter word from words.py at start
- [ ] **GAME-02**: Game displays 5x6 grid of cells for letter guesses
- [ ] **GAME-03**: Game allows player to enter up to 5 letters per guess
- [ ] **GAME-04**: Game prevents entering more than 5 letters per guess
- [x] **GAME-05**: Game validates guess against words.py dictionary before accepting
- [x] **GAME-06**: Game rejects invalid (non-dictionary) words
- [x] **GAME-07**: Game tracks remaining attempts (6 total)
- [x] **GAME-08**: Game ends when correct word guessed or 6 attempts exhausted

### Visual Feedback

- [ ] **VIS-01**: Empty cells show light gray border with empty background
- [ ] **VIS-02**: Cells show green background when letter is correct position
- [ ] **VIS-03**: Cells show yellow/amber background when letter exists but wrong position
- [ ] **VIS-04**: Cells show gray background when letter not in target word
- [ ] **VIS-05**: Cell colors update immediately after guess submission
- [ ] **VIS-06**: Visual design matches NYTimes Wordle aesthetic (colors, spacing, grid structure)

### Keyboard Interface

- [ ] **KEY-01**: On-screen QWERTY keyboard displays all letter keys
- [ ] **KEY-02**: Keyboard includes backspace key
- [ ] **KEY-03**: Keyboard includes enter key
- [ ] **KEY-04**: Keyboard keys reflect same color feedback as grid (gray/yellow/green)
- [ ] **KEY-05**: Keyboard updates colors after each guess submission

### Game Logic

- [ ] **LOGIC-01**: Correctly handles duplicate letters in guesses
- [ ] **LOGIC-02**: Correctly handles duplicate letters in target word
- [x] **LOGIC-03**: Letter status priority: green > yellow > gray
- [ ] **LOGIC-04**: Multiple instances of same letter get independent evaluation

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Daily Puzzle

- **DAILY-01**: Game selects same word for all players on a given day
- **DAILY-02**: Game prevents replaying same day's puzzle
- **DAILY-03**: Game resets to new word at midnight

### Statistics

- **STAT-01**: Game tracks win/loss record across sessions
- **STAT-02**: Game displays current win streak
- **STAT-03**: Game shows guess distribution histogram
- **STAT-04**: Statistics persist between game sessions

### Social Features

- **SOCIAL-01**: Player can copy emoji grid representation of game result
- **SOCIAL-02**: Emoji grid uses 🟩🟨⬜ symbols matching color feedback
- **SOCIAL-03**: Emoji grid hides actual letters (spoiler-free)

### Themes

- **THEME-01**: Colorblind mode with alternative color schemes
- **THEME-02**: Dark theme option
- **THEME-03**: Light theme option (default)

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Unlimited puzzles per day | Destroys scarcity model that made Wordle viral; anti-feature |
| Hints or help mode | Core gameplay is pure deduction; hints undermine challenge |
| 4-letter or 6-letter variants | Classic 5-letter format is the standard; avoid fragmentation |
| Multiplayer or competitive modes | Single-player focus keeps complexity manageable |
| External word APIs | words.py provides complete dictionary; no network dependency |
| Mobile app version | Terminal UI is the constraint; separate project if needed |
| Timer or speed challenges | Wordle is contemplative, not time-pressured |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| GAME-01 | Phase 1 | Complete |
| GAME-02 | Phase 2 | Pending |
| GAME-03 | Phase 3 | Pending |
| GAME-04 | Phase 3 | Pending |
| GAME-05 | Phase 1 | Complete |
| GAME-06 | Phase 1 | Complete |
| GAME-07 | Phase 1 | Complete |
| GAME-08 | Phase 1 | Complete |
| VIS-01 | Phase 2 | Pending |
| VIS-02 | Phase 2 | Pending |
| VIS-03 | Phase 2 | Pending |
| VIS-04 | Phase 2 | Pending |
| VIS-05 | Phase 2 | Pending |
| VIS-06 | Phase 2 | Pending |
| KEY-01 | Phase 3 | Pending |
| KEY-02 | Phase 3 | Pending |
| KEY-03 | Phase 3 | Pending |
| KEY-04 | Phase 3 | Pending |
| KEY-05 | Phase 3 | Pending |
| LOGIC-01 | Phase 1 | Pending |
| LOGIC-02 | Phase 1 | Pending |
| LOGIC-03 | Phase 1 | Complete |
| LOGIC-04 | Phase 1 | Pending |

**Coverage:**
- v1 requirements: 19 total
- Mapped to phases: 19 ✓
- Unmapped: 0 ✓

---
*Requirements defined: 2025-03-14*
*Last updated: 2026-03-14 after roadmap creation*
