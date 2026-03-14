# Wordle CLI

A terminal-based Wordle game built with Python and Textual.

## Installation

```bash
pip install -e .
```

## How to Play

```bash
python -m wordle_cli
```

### Controls

| Key | Action |
|-----|--------|
| `A-Z` | Type letters |
| `Backspace` | Delete last letter |
| `Enter` | Submit guess |
| `Ctrl+R` | Start new game |
| `Ctrl+Q` | Quit game |

### Rules

- Guess the 5-letter word in 6 attempts
- **Green** = Correct letter in correct position
- **Yellow** = Correct letter in wrong position
- **Gray** = Letter not in word

## Running Tests

```bash
pytest tests/
```
