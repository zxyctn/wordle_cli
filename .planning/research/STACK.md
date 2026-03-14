# Technology Stack

**Project:** Wordle CLI
**Researched:** 2026-03-14
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.10+ | Runtime environment | Modern Python features (pattern matching, type hints), excellent async support, required by Textual |
| Textual | 8.1.1+ | Terminal UI framework | Industry-standard Python TUI framework with excellent widget support, built-in grid layouts, keyboard handling, and CSS-like styling. Active development (v8.1.1 released Mar 2026). |
| textual-dev | latest | Development tooling | Provides dev console for debugging, live preview, and essential development tools for Textual apps |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | 7.0+ | Testing framework | Core testing (unit tests for game logic) |
| pytest-asyncio | 0.21+ | Async test support | Testing Textual UI interactions (required for async tests) |
| pytest-textual-snapshot | latest | Visual regression testing | Optional: Snapshot testing UI appearance to catch visual bugs |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| textual console | Live debugging | Run `textual console` in separate terminal for real-time app inspection |
| textual run --dev | Hot reload | Auto-restart app on file changes during development |
| mypy | Type checking | Optional but recommended for ports/adapters architecture |
| ruff | Linting/formatting | Modern, fast Python linter (replaces Black + flake8) |

## Installation

```bash
# Core dependencies
pip install textual textual-dev

# Testing dependencies
pip install pytest pytest-asyncio

# Optional: snapshot testing for UI
pip install pytest-textual-snapshot

# Development tools (optional)
pip install mypy ruff
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Textual | Rich (direct) | Simple output-only displays with no interaction |
| Textual | curses | Legacy codebases or need raw terminal control (significantly harder to use) |
| Textual | urwid | Existing urwid codebase (unmaintained since 2021, avoid for new projects) |
| pytest | unittest | Already using unittest framework (pytest can run unittest tests anyway) |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| curses (directly) | Low-level, difficult API, platform inconsistencies, no modern widgets | Textual (built on top of Rich, handles all the hard parts) |
| urwid | Last release 2021, no active maintenance, outdated patterns | Textual (modern, actively developed) |
| prompt_toolkit | Designed for prompts/CLIs, not full TUI apps, complex grid layouts difficult | Textual (purpose-built for full-screen TUI applications) |
| Textual < 7.0 | Breaking changes in v7.0+, missing features | Textual 8.1.1+ (current stable) |
| asyncio.run() in tests | Won't work with pytest-asyncio, causes event loop conflicts | pytest-asyncio with `asyncio_mode = auto` |

## Stack Patterns by Project Type

**For Simple Games (like Wordle):**
- Use Textual's built-in widgets (Static for grid cells, Container for layout)
- Single-file app or simple module structure
- Minimal dependencies (textual + pytest only)

**For Complex TUI Applications:**
- Add pytest-textual-snapshot for visual regression testing
- Use custom widgets (subclass Textual widgets)
- Separate CSS files for styling
- Add mypy for type safety in larger codebases

**For Production Deployment:**
- Pin exact versions in requirements.txt
- Use textual-serve to deploy to web browsers
- Consider packaging with PyInstaller or similar for standalone executables

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| Textual 8.x | Python 3.10+ | Breaking changes from v7.x: `Select.BLANK` → `Select.NULL` |
| pytest-asyncio | pytest 7.0+ | Set `asyncio_mode = auto` in pytest.ini to avoid decorators |
| textual-dev | Textual 8.x | Always use matching major version |

## Textual-Specific Patterns

**Widget Architecture:**
- Use `Static` widget for grid cells (can style with CSS)
- Use `Container` with grid layout for 5x6 Wordle grid
- Use `Label` or custom widget for keyboard display
- Leverage Textual's reactive attributes for state updates

**Styling:**
- Use TCSS (Textual CSS) for colors, borders, spacing
- Define CSS inline in `CSS` class variable or external file
- Color palette: green (#6aaa64), yellow (#c9b458), gray (#787c7e) for Wordle

**Testing:**
- Use `app.run_test()` context manager (not `app.run()`)
- `async with app.run_test() as pilot:` returns Pilot for interactions
- `await pilot.press("key")` for keyboard input
- `await pilot.click("#widget-id")` for mouse clicks
- `await pilot.pause()` to wait for message processing

**Development Workflow:**
1. Run `textual console` in one terminal
2. Run `textual run --dev app.py` in another
3. Live debugging output appears in console
4. Hot reload on file changes

## Python Version Requirements

**Minimum:** Python 3.10
**Recommended:** Python 3.11+ or 3.12

**Rationale:**
- Textual requires Python 3.10+ (uses modern type hints, pattern matching)
- Python 3.11+ offers 10-25% performance improvements
- Python 3.12 offers better asyncio performance (helpful for Textual)
- Python 3.10 still widely available if broader compatibility needed

## Sources

- [Textual Official Documentation](https://textual.textualize.io/) — Framework capabilities, widget gallery, testing guide (HIGH confidence)
- [Textual GitHub Releases](https://github.com/Textualize/textual/releases) — Current version v8.1.1 (Mar 10, 2026), version compatibility (HIGH confidence)
- [pytest Documentation](https://docs.pytest.org/) — Testing framework features (HIGH confidence)
- [Textual Testing Guide](https://textual.textualize.io/guide/testing/) — Testing patterns, Pilot API, async testing (HIGH confidence)

---
*Stack research for: Python Terminal UI Game*
*Researched: 2026-03-14*
