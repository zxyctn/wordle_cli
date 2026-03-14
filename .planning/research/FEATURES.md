# Feature Research

**Domain:** Wordle-style word guessing game (CLI implementation)
**Researched:** 2026-03-14
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| 5-letter word target | Core Wordle mechanic | LOW | Industry standard; deviating breaks "Wordle" identity |
| 6 guess attempts | Standard difficulty balance | LOW | More attempts = too easy, fewer = frustrating |
| Color-coded feedback (green/yellow/gray) | Visual language all players know | LOW | Green = correct position, yellow = wrong position, gray = not in word |
| Grid display (5x6) | Expected visual representation | MEDIUM | Shows guess history; helps players track patterns |
| Valid word enforcement | Prevents random letter guessing | LOW | Must validate against dictionary; part of the challenge |
| On-screen keyboard with feedback | Players expect to see tested letters | MEDIUM | Keyboard reflects same colors as grid; prevents retesting letters |
| Single daily puzzle | Scarcity creates habit and shareability | MEDIUM | Multiple puzzles would dilute the "everyone solves same word" community aspect |
| Letter position validation | Correct letters marked per position | MEDIUM | Handles duplicate letters correctly (e.g., "ROBOT" with multiple Os) |
| Input constraints (5 letters only) | Enforces game rules | LOW | Prevents invalid inputs |
| Win/loss detection | Game must end appropriately | LOW | Win on correct guess OR loss after 6 attempts |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Hard mode | Increases challenge for experienced players | LOW | Forces use of revealed hints in subsequent guesses |
| Colorblind mode (high contrast) | Accessibility for colorblind users | LOW | Replace green/yellow with orange/blue or symbols |
| Dark theme | Reduces eye strain, modern UX expectation | LOW | Many TUI apps offer theme switching |
| Statistics tracking | Engagement through progress metrics | MEDIUM | Track win rate, current streak, guess distribution |
| Shareable results (emoji grid) | Social proof and virality driver | LOW | Text-based results without spoilers (🟩🟨⬜) |
| Daily streak counter | Habit formation and retention | MEDIUM | Encourages daily play; depends on statistics feature |
| Word definition on completion | Educational value | MEDIUM | Show definition after win/loss (requires dictionary API or data) |
| Custom difficulty settings | Personalization for different skill levels | MEDIUM | Could include word length variants, attempt limits |
| Offline play capability | CLI advantage over web versions | LOW | Works without internet; uses local word list |
| Multiple language support | Expands audience | HIGH | Requires word lists for each language |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Unlimited puzzles per day | "I want to play more!" | Destroys scarcity model; reduces shareability; creates addiction concerns | Offer practice mode with random words (non-daily) |
| Hints or help system | Players stuck on hard words | Removes the pure deduction challenge; cheapens victories | Provide optional hard mode instead for challenge seekers |
| Variable word lengths in same puzzle | "Add variety" | Breaks mental model; confuses grid display; dilutes brand | Keep 5-letter standard; create separate game modes if needed |
| Multiplayer competitive mode | "I want to race friends" | Adds complexity; deviates from meditative solo experience | Share results for friendly competition instead |
| Custom word selection by players | "Let me choose the word" | Ruins surprise; enables cheating; breaks daily puzzle model | Allow custom challenges as separate mode only |
| Leaderboards and scoring | Gamification request | Creates pressure/anxiety; deviates from casual, daily ritual | Keep personal stats only; emphasize streaks over competition |
| Infinite time per guess | "Don't rush me" | Enables cheating via lookup tools; reduces engagement | No time limit is already the standard; maintain this |
| Save/resume mid-puzzle | "I need to pause" | Encourages cheating; reduces commitment | Puzzle state can persist but shouldn't span multiple sessions |

## Feature Dependencies

```
[Valid Word Enforcement]
    └──requires──> [Word Dictionary/List]

[Statistics Tracking]
    └──requires──> [Persistent Storage]
    └──requires──> [Win/Loss Detection]

[Daily Streak Counter]
    └──requires──> [Statistics Tracking]
    └──requires──> [Date/Time Tracking]

[Shareable Results]
    └──requires──> [Color-coded Feedback]
    └──requires──> [Clipboard Access OR Text Export]

[Hard Mode]
    └──requires──> [Letter Position Validation]
    └──enhances──> [Color-coded Feedback]

[On-screen Keyboard]
    └──requires──> [Color-coded Feedback]
    └──enhances──> [Grid Display]

[Colorblind Mode]
    ──conflicts──> [Standard Color Scheme] (must toggle)

[Dark Theme]
    ──conflicts──> [Light Theme] (must toggle)
```

### Dependency Notes

- **Valid Word Enforcement requires Word Dictionary:** Cannot validate guesses without a word list; PROJECT.md confirms `words.py` already exists
- **Statistics Tracking requires Persistent Storage:** Need to save data between sessions (file-based for CLI)
- **Daily Streak Counter requires Statistics Tracking:** Streaks are a subset of overall statistics; also needs date tracking to detect consecutive days
- **Shareable Results require Color-coded Feedback:** Can't generate emoji grid without knowing guess outcomes
- **Hard Mode enhances Color-coded Feedback:** Uses revealed hints to constrain future guesses
- **Colorblind Mode conflicts with Standard Color Scheme:** These are mutually exclusive display modes; users toggle between them

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate the concept.

- [x] **5-letter word target from dictionary** — Core game mechanic
- [x] **6 guess attempts** — Standard difficulty
- [x] **Color-coded feedback (green/yellow/gray)** — Essential visual language
- [x] **5x6 grid display** — Shows guess history
- [x] **Valid word enforcement** — Prevents random guessing
- [x] **On-screen keyboard with feedback** — Expected UX element
- [x] **Letter position validation** — Handles duplicate letters correctly
- [x] **Input constraints (5 letters)** — Enforces rules
- [x] **Win/loss detection** — Completes game loop
- [ ] **Basic TUI layout** — Functional Textual interface

**Rationale:** These features constitute the complete core Wordle experience. Without any of these, the game is broken or unrecognizable as Wordle. Note: "Single daily puzzle" is table stakes but deferred to v1.1 for MVP simplicity.

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] **Single daily puzzle** — v1.1: Adds scarcity model; requires date-based word selection
- [ ] **Statistics tracking** — v1.2: Track wins, losses, streak; requires persistent storage
- [ ] **Shareable results (emoji grid)** — v1.2: Enables social sharing; drives virality
- [ ] **Dark theme** — v1.3: Modern UX expectation for CLI apps
- [ ] **Colorblind mode** — v1.3: Accessibility; should ship with dark theme
- [ ] **Hard mode** — v1.4: For experienced players; simple constraint addition

**Triggers:**
- Daily puzzle: After core gameplay validated (need date persistence)
- Statistics: After daily puzzle implemented (tracks daily performance)
- Shareable results: Alongside statistics (natural pairing)
- Themes: After gameplay stable (polish phase)

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] **Word definition on completion** — Requires dictionary integration or API
- [ ] **Practice mode (unlimited non-daily puzzles)** — Addresses "I want to play more" without breaking daily model
- [ ] **Custom difficulty settings** — Once user base established and requests clarify needs
- [ ] **Multiple language support** — Requires significant word list curation
- [ ] **Guess distribution histogram** — Advanced statistics feature
- [ ] **Achievement system** — Gamification for retention (careful: avoid anti-feature territory)

**Why defer:**
- These add complexity without being core to the Wordle experience
- Need user feedback to validate which would add most value
- Dictionary/API integrations add dependencies
- Language support requires significant content work

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| 5-letter word + 6 attempts | HIGH | LOW | P1 |
| Color-coded feedback | HIGH | LOW | P1 |
| Grid display (5x6) | HIGH | MEDIUM | P1 |
| On-screen keyboard | HIGH | MEDIUM | P1 |
| Valid word enforcement | HIGH | LOW | P1 |
| Letter position validation | HIGH | MEDIUM | P1 |
| Win/loss detection | HIGH | LOW | P1 |
| Input constraints | HIGH | LOW | P1 |
| Single daily puzzle | HIGH | MEDIUM | P2 |
| Statistics tracking | MEDIUM | MEDIUM | P2 |
| Shareable results | MEDIUM | LOW | P2 |
| Dark theme | MEDIUM | LOW | P2 |
| Colorblind mode | MEDIUM | LOW | P2 |
| Hard mode | LOW | LOW | P2 |
| Word definition | LOW | MEDIUM | P3 |
| Practice mode | MEDIUM | MEDIUM | P3 |
| Multiple languages | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch (MVP)
- P2: Should have, add when possible (post-MVP enhancements)
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | NYTimes Wordle (web) | Termo (Brazilian clone) | Typical CLI Clone | Our Approach |
|---------|----------------------|------------------------|-------------------|--------------|
| Daily puzzle | ✅ Single puzzle/day | ✅ Single puzzle/day | ❌ Often unlimited | ✅ Implement in v1.1 |
| Color feedback | ✅ Green/yellow/gray | ✅ Green/yellow/gray | ✅ Standard | ✅ Core feature |
| Statistics | ✅ Comprehensive stats | ✅ With server sync | ⚠️ Often missing | ✅ v1.2 with local storage |
| Shareable results | ✅ Emoji grid | ✅ Emoji grid | ⚠️ Inconsistent | ✅ v1.2 text-based |
| Keyboard display | ✅ On-screen | ✅ On-screen | ⚠️ Often text-only | ✅ TUI widget |
| Themes | ✅ Dark + colorblind | ✅ Theme options | ❌ Rarely | ✅ v1.3 |
| Hard mode | ✅ Optional toggle | ❌ Not present | ❌ Rarely | ✅ v1.4 |
| Hints/help | ❌ None (good) | ❌ None (good) | ⚠️ Some add this | ❌ Avoid (anti-feature) |
| Multiple puzzles | ❌ One per day | ❌ One per day | ✅ Common mistake | ⚠️ Practice mode only (v2) |
| WordleBot analysis | ✅ Post-game analysis | ❌ Not present | ❌ Not present | ❌ Out of scope |

**Key insights:**
- **Daily puzzle scarcity** is what made NYTimes Wordle viral — many clones miss this
- **Shareable results** drove social media spread — essential for virality
- **Statistics** drive engagement and habit formation
- **CLI advantage:** Offline play, no ads, fast startup
- **Avoid common clone mistakes:** Unlimited puzzles, hints, overgamification

## Sources

### Primary Research
- **Wikipedia: Wordle** (https://en.wikipedia.org/wiki/Wordle) — Comprehensive history, gameplay mechanics, feature evolution
  - Confidence: HIGH (well-cited article with 89+ references)
  - Key findings: Color-coded feedback system, duplicate letter handling, acquisition by NYT, feature changes over time

### Verified Patterns
- **Single daily puzzle** — Confirmed as core to viral success (Wikipedia, NYT acquisition articles)
- **Shareable emoji results** — Added December 2021, catalyst for viral growth (Wikipedia section on "Rise in popularity")
- **Hard mode** — Official feature in original Wordle (The Verge reference in Wikipedia)
- **Colorblind accessibility** — Standard feature in NYT version (Wikipedia gameplay section)

### Domain Knowledge (Training Data)
- **Grid display patterns** — Standard 5x6 layout across all implementations
- **Duplicate letter handling** — Critical mechanic often implemented incorrectly in clones
- **Scarcity model** — One puzzle per day creates anticipation and community discussion
- **Anti-features** — Unlimited play, hints, and competitive modes consistently noted as deviating from successful formula

### Confidence Assessment
- **Table stakes features:** HIGH confidence (universally present in all successful Wordle implementations)
- **Differentiators:** MEDIUM-HIGH confidence (based on NYT Wordle features and successful clones)
- **Anti-features:** HIGH confidence (well-documented mistakes in failed clones and explicitly avoided by original creator)

---
*Feature research for: Wordle CLI*
*Researched: 2026-03-14*
