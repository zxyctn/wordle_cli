# Project Research Summary

**Project:** Wordle CLI
**Domain:** Terminal-based word guessing game (Wordle clone)
**Researched:** 2026-03-14
**Confidence:** HIGH

## Executive Summary

Wordle CLI is a terminal-based implementation of the popular Wordle word-guessing game using Python and the Textual framework. The recommended approach follows hexagonal (ports & adapters) architecture with pure domain logic separated from UI concerns. The core stack consists of Python 3.10+, Textual 8.1.1+ for the TUI framework, and pytest with async support for testing. This combination provides the modern reactive UI capabilities needed for an engaging terminal experience while maintaining clean separation between game rules and presentation.

The critical success factor is implementing the complete Wordle experience: 5-letter words, 6 attempts, color-coded feedback (green/yellow/gray), grid display, and on-screen keyboard. These table stakes features are non-negotiable — missing any breaks user expectations. The architecture must keep game logic pure and testable, using Textual's reactive attributes for state synchronization between domain and UI. The main technical risks involve properly handling duplicate letters in the evaluation logic and managing Textual's async event model, both mitigated through TDD and following documented Textual patterns.

The roadmap should prioritize building the domain layer first (game engine, evaluator, models) before any UI work, enabling fast test-driven development of core rules. The presentation layer follows, leveraging Textual's widget composition and reactive updates. Post-MVP enhancements (daily puzzle, statistics, themes) can be added incrementally without disrupting the core architecture.

## Key Findings

### Recommended Stack

Python 3.10+ with Textual 8.1.1+ provides the optimal foundation for a modern terminal UI game. Textual is the industry-standard Python TUI framework with excellent widget support, built-in grid layouts, keyboard handling, and CSS-like styling through TCSS. The framework's reactive attribute system enables declarative UI updates without manual refresh calls, significantly simplifying state synchronization.

**Core technologies:**
- **Python 3.10+**: Runtime environment — modern features (pattern matching, type hints), excellent async support required by Textual
- **Textual 8.1.1+**: Terminal UI framework — industry-standard Python TUI with reactive widgets, grid layouts, and CSS-like styling
- **textual-dev**: Development tooling — provides debug console, live preview, hot reload for efficient development
- **pytest 7.0+ with pytest-asyncio**: Testing framework — essential for TDD approach; pytest-asyncio required for testing Textual's async widgets

**Critical version requirements:**
- Python 3.10 minimum (Textual dependency), Python 3.11+ recommended for performance
- Textual 8.x has breaking changes from 7.x (`Select.BLANK` → `Select.NULL`)
- pytest-asyncio requires `asyncio_mode = auto` in pytest.ini

**Development workflow:**
- Run `textual console` in one terminal for live debugging
- Run `textual run --dev app.py` for hot reload during development
- Use `app.run_test()` context manager for widget testing with Pilot API

### Expected Features

The Wordle feature landscape divides into three tiers: table stakes (must have), differentiators (competitive advantage), and anti-features (avoid).

**Must have (table stakes):**
- 5-letter word target with 6 guess attempts — core Wordle mechanic, non-negotiable
- Color-coded feedback (green/yellow/gray) — visual language all players know
- 5x6 grid display — shows guess history, essential for pattern tracking
- Valid word enforcement — prevents random letter guessing, requires dictionary
- On-screen keyboard with feedback — players expect to see tested letters
- Letter position validation — handles duplicate letters correctly (critical mechanic)
- Input constraints (5 letters only) — enforces game rules
- Win/loss detection — completes game loop

**Should have (competitive):**
- Single daily puzzle — creates scarcity and shareability (v1.1)
- Statistics tracking — engagement through win rate, streaks (v1.2)
- Shareable results (emoji grid) — social proof driver, viral feature (v1.2)
- Dark theme & colorblind mode — accessibility and modern UX (v1.3)
- Hard mode — increases challenge for experienced players (v1.4)
- Offline play capability — CLI advantage over web versions

**Defer (v2+):**
- Word definition on completion — educational value but requires dictionary API
- Practice mode (unlimited puzzles) — addresses "play more" without breaking daily model
- Custom difficulty settings — needs user feedback to validate requirements
- Multiple language support — significant word list curation effort

**Anti-features to avoid:**
- Unlimited daily puzzles — destroys scarcity model and shareability
- Hints/help system — removes pure deduction challenge
- Variable word lengths in same puzzle — breaks mental model
- Multiplayer competitive mode — adds complexity, deviates from meditative experience
- Leaderboards — creates pressure/anxiety vs casual daily ritual

### Architecture Approach

The recommended architecture follows hexagonal (ports & adapters) pattern with clear separation between domain logic, infrastructure adapters, and presentation layer. This enables fast unit testing of game rules without UI framework overhead and potential reuse of logic in other interfaces (web, mobile).

**Major components:**
1. **Domain Layer** — Pure game logic with zero Textual dependencies: GameEngine (orchestrates rules), GuessEvaluator (compares guess vs target), GameState (immutable state), LetterStatus enum, and abstract ports (WordRepository interface)
2. **Infrastructure Layer** — Adapters implementing domain ports: InMemoryWordRepository (reads words.py list), future FileStatsStore for persistence
3. **Presentation Layer** — Textual App and custom widgets: WordleApp (UI orchestrator with reactive attributes), GridWidget (6x5 cells), KeyboardWidget (QWERTY with feedback), using message passing for loose coupling

**Key patterns:**
- **Reactive UI updates** — Textual reactive attributes trigger automatic widget refresh when state changes
- **Message passing** — Widgets emit custom messages that bubble up; decouples widget implementation from action handling
- **Immutable domain models** — GameState and GuessResult are frozen dataclasses for predictable state management
- **Build order** — Domain layer first (models → ports → evaluator → engine), then infrastructure (adapters), finally presentation (widgets → app)

**Data flow:** User input → Input Widget → GuessSubmitted message → App validates with GameEngine → GameEngine.process_guess() returns GuessResult → App updates game_state reactive → GridWidget and KeyboardWidget watch methods auto-recompose

### Critical Pitfalls

**Note:** PITFALLS.md was not generated by the research phase. The following critical pitfalls are derived from ARCHITECTURE.md anti-patterns and STACK.md warnings:

1. **Putting game logic in widgets** — Violates single responsibility; impossible to test rules without UI; can't reuse logic. **Prevention:** Keep domain/ pure with zero Textual imports; all game rules in GameEngine/GuessEvaluator
2. **Direct coupling to words.py** — Hard to test with different word lists; can't swap data sources. **Prevention:** Use WordRepository port/adapter pattern; inject dependency into GameEngine
3. **Storing widget references in domain** — Inverts dependency direction; tight coupling prevents reuse. **Prevention:** Domain returns results, doesn't update UI; app layer handles widget updates via reactive attributes
4. **Duplicate letter handling errors** — Common implementation bug in Wordle clones (e.g., "ROBOT" with two Os). **Prevention:** TDD the GuessEvaluator with comprehensive duplicate letter test cases
5. **Async event loop conflicts in tests** — Using `asyncio.run()` with pytest-asyncio causes event loop errors. **Prevention:** Use `app.run_test()` context manager; set `asyncio_mode = auto` in pytest.ini

## Implications for Roadmap

Based on research, suggested phase structure prioritizes domain-first development to establish testable game rules before UI complexity:

### Phase 1: Core Domain Layer
**Rationale:** Pure Python game logic with zero dependencies enables fast TDD of critical rules. Must establish correct letter evaluation logic (especially duplicate handling) before building UI.

**Delivers:** Fully tested game engine that can validate guesses, evaluate letter positions, track game state, and detect win/loss conditions. No UI, pure domain.

**Addresses:** 
- Letter position validation (handles duplicates correctly)
- Valid word enforcement (WordRepository interface)
- Win/loss detection
- Core game state management

**Avoids:** 
- Game logic in widgets (keep domain pure)
- Direct coupling to words.py (use port/adapter)
- Duplicate letter bugs (TDD with comprehensive cases)

**Build order:**
1. `domain/models.py` — LetterStatus enum, GameState, GuessResult dataclasses
2. `domain/ports.py` — WordRepository abstract interface
3. `domain/evaluator.py` — GuessEvaluator with duplicate letter handling
4. `domain/game_engine.py` — GameEngine orchestration
5. Comprehensive unit tests (fast, no UI framework)

### Phase 2: Infrastructure Adapters
**Rationale:** Implements domain ports with concrete adapters. Simple in-memory implementation sufficient for MVP; architecture supports future enhancements (API word lists, file-based stats).

**Delivers:** Working word repository that loads from words.py and provides validation/selection capabilities.

**Uses:** 
- Python standard library (random for word selection)
- words.py game_words array (already exists per PROJECT.md)

**Implements:** 
- InMemoryWordRepository adapter implementing WordRepository port
- Integration tests validating adapter behavior

**Dependency:** Requires Phase 1 domain/ports.py interface

### Phase 3: Basic Textual UI
**Rationale:** Establishes Textual app structure and core widgets without polish. Focus on functional interaction: type guess, submit, see results. Validates UI architecture before adding complexity.

**Delivers:** Minimal working TUI — grid displays guesses with color feedback, keyboard shows letter status, input accepts 5-letter words.

**Addresses:**
- Grid display (5x6)
- Color-coded feedback (green/yellow/gray)
- On-screen keyboard with feedback
- Input constraints (5 letters only)

**Uses:**
- Textual 8.1.1+ reactive attributes for state sync
- Custom widgets (GridWidget, KeyboardWidget)
- Message passing for input events
- TCSS for Wordle color palette (#6aaa64 green, #c9b458 yellow, #787c7e gray)

**Implements:**
- `widgets/cell.py` — LetterCell (single grid cell)
- `widgets/grid.py` — GuessGridWidget (composes 30 cells)
- `widgets/keyboard.py` — OnScreenKeyboard with letter status
- `app.py` — WordleApp wires domain to widgets

**Avoids:**
- Widget references in domain (domain returns results only)
- Manual refresh calls (use reactive attributes)
- Async test pitfalls (use app.run_test() context manager)

### Phase 4: Game Flow & Polish
**Rationale:** Completes MVP gameplay loop with proper feedback, error handling, and game-over states. Makes it feel like Wordle.

**Delivers:** Complete playable game with win/loss screens, invalid word feedback, restart capability.

**Addresses:**
- Win/loss detection (game over states)
- Valid word enforcement (reject invalid guesses)
- 5-letter word target and 6 guess attempts (complete game rules)

**Enhancements:**
- Modal/screen for win/loss messages
- Invalid guess feedback (not in word list)
- Restart game functionality
- Visual polish (borders, spacing, animations)

### Phase 5: Daily Puzzle (v1.1)
**Rationale:** Adds scarcity model that made Wordle viral. Requires date-based word selection and basic persistence. Natural extension after core gameplay proven.

**Delivers:** Single puzzle per day, deterministic based on date, same word for all players.

**Addresses:**
- Single daily puzzle (table stakes feature deferred from MVP)

**Implementation:**
- Date-based seed for word selection
- Simple persistence (track last played date)
- Prevent multiple plays per day

### Phase 6: Statistics & Sharing (v1.2)
**Rationale:** Engagement and virality features. Statistics drive habit formation; shareable results drove Wordle's social media spread. Natural pairing.

**Delivers:** Win rate, current streak, guess distribution; emoji grid export for sharing.

**Addresses:**
- Statistics tracking (win rate, streaks)
- Shareable results (emoji grid 🟩🟨⬜)

**Implementation:**
- StatsRepository port + FileStatsStore adapter (JSON or SQLite)
- Emoji grid generator (uses GuessResult letter statuses)
- Clipboard integration or text file export

**Dependency:** Requires Phase 5 daily puzzle (stats track daily performance)

### Phase 7: Themes & Accessibility (v1.3)
**Rationale:** Modern UX expectations and accessibility. Low implementation cost with Textual's CSS system. Should ship together for complete accessibility story.

**Delivers:** Dark theme toggle, colorblind-friendly mode (high contrast or symbols).

**Addresses:**
- Dark theme (modern UX expectation)
- Colorblind mode (accessibility)

**Implementation:**
- TCSS theme variants
- Toggle command or settings screen
- Orange/blue palette or symbols for colorblind mode

### Phase Ordering Rationale

- **Domain-first approach** — Building pure game logic before UI enables fast TDD without framework overhead. Critical for getting duplicate letter evaluation correct.
- **Incremental UI complexity** — Phase 3 establishes widgets/reactive patterns with minimal features; Phase 4 completes MVP; later phases add engagement features.
- **Dependency-driven sequencing** — Statistics (Phase 6) requires daily puzzle (Phase 5); daily puzzle requires core gameplay (Phases 1-4).
- **Hexagonal architecture benefits** — Clear port/adapter boundaries in Phases 1-2 enable easy feature additions (stats persistence, API word lists) without domain changes.
- **Risk mitigation** — TDD in Phase 1 prevents duplicate letter bugs; pure domain prevents widget coupling; adapter pattern prevents words.py coupling.

### Research Flags

Phases with standard patterns (skip research-phase):
- **Phase 1 (Domain Layer):** Well-established game logic patterns; core Wordle mechanics extensively documented
- **Phase 2 (Adapters):** Simple in-memory implementation, standard repository pattern
- **Phase 3 (Textual UI):** Textual official docs provide comprehensive widget/reactive patterns; TUI game examples available
- **Phase 4 (Game Flow):** Standard UX patterns for modal dialogs and game state transitions
- **Phase 5 (Daily Puzzle):** Simple date-based seeding, well-documented pattern
- **Phase 6 (Statistics):** Standard persistence patterns, emoji grid generation straightforward
- **Phase 7 (Themes):** Textual CSS theming well-documented

**No phases require deeper research.** All patterns are well-established with high-confidence sources (Textual official docs, standard Wordle mechanics, common software patterns).

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Textual official documentation comprehensive; version compatibility clearly documented; testing patterns established |
| Features | HIGH | Well-cited Wikipedia article (89+ references); NYT Wordle feature set public; clear table stakes vs differentiators |
| Architecture | HIGH | Textual official docs for reactive patterns; hexagonal architecture standard practice; clear component boundaries |
| Pitfalls | MEDIUM | Derived from architecture anti-patterns and stack warnings; PITFALLS.md not generated during research phase |

**Overall confidence:** HIGH

The research is based on authoritative sources (Textual official documentation, Wikipedia with 89+ references, established software patterns). The main gap is the missing PITFALLS.md file, but critical pitfalls were extracted from architecture anti-patterns and stack warnings.

### Gaps to Address

- **PITFALLS.md not generated:** The parallel research phase did not create this file. Critical pitfalls have been inferred from ARCHITECTURE.md anti-patterns and STACK.md warnings, but a dedicated pitfalls analysis would strengthen the research. Consider generating this during Phase 1 planning if needed.

- **Duplicate letter edge cases:** While research identifies this as critical, detailed test cases for all edge scenarios (multiple same letters in different positions) should be documented during Phase 1 TDD.

- **Textual performance at scale:** Research doesn't address performance implications of 30+ reactive widgets (6x5 grid). Monitor during Phase 3 development; Textual docs indicate this should be fine, but validate in practice.

- **Persistence strategy details:** Phase 6 (statistics) defers decision between JSON file vs SQLite. Evaluate during Phase 6 planning based on data complexity (simple key-value = JSON; complex queries = SQLite).

## Sources

### Primary (HIGH confidence)
- [Textual Official Documentation](https://textual.textualize.io/) — Framework capabilities, widget gallery, reactive attributes, testing guide with Pilot API
- [Textual GitHub Releases](https://github.com/Textualize/textual/releases) — Current version v8.1.1 (Mar 10, 2026), version compatibility notes
- [pytest Documentation](https://docs.pytest.org/) — Testing framework features, pytest-asyncio integration
- [Wikipedia: Wordle](https://en.wikipedia.org/wiki/Wordle) — Comprehensive history, gameplay mechanics, feature evolution (89+ references)

### Secondary (MEDIUM confidence)
- [Wikipedia - Hexagonal Architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) — Ports & adapters pattern, separation of concerns
- Domain knowledge (training data) — Grid display patterns, duplicate letter handling, scarcity model, anti-features in failed clones

### Coverage
- **Stack research:** Textual framework, Python version requirements, testing tools, development workflow
- **Feature research:** Table stakes features, differentiators, anti-features, MVP definition, competitor analysis
- **Architecture research:** Hexagonal pattern, component boundaries, Textual reactive patterns, data flow, project structure

---
*Research completed: 2026-03-14*
*Ready for roadmap: yes*
