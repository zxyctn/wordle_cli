# 🎮 Wordle CLI

A beautiful terminal-based Wordle game built with Python and Textual.

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **Classic Wordle Gameplay** - Guess the 5-letter word in 6 attempts
- **Color-Coded Feedback** - Visual hints using border and text colors
  - 🟢 **Green** - Correct letter in correct position
  - 🟡 **Yellow** - Correct letter in wrong position
  - ⬜ **Gray** - Letter not in word
- **Smart Keyboard** - On-screen keyboard that updates with your guesses
- **Clean UI** - Centered, minimalist design inspired by the original Wordle
- **Toast Notifications** - Helpful messages for errors and game status
- **Instant Restart** - Start a new game anytime with `Ctrl+R`

## 🚀 Installation

### Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install textual
```

Or install from the project directory:

```bash
pip install -e .
```

## 🎯 How to Play

### Start the Game

Run the game from the project directory:

```bash
python -m src.wordle_cli.app
```

### Game Rules

1. You have **6 attempts** to guess a 5-letter word
2. Type your guess using your keyboard (A-Z)
3. Press **Enter** to submit your guess
4. After each guess, the colors will change:
   - **Green border/text** = Letter is in the word and in the correct position
   - **Yellow border/text** = Letter is in the word but in the wrong position
   - **Gray border/text** = Letter is not in the word at all

### Controls

| Key | Action |
|-----|--------|
| `A-Z` | Type letters |
| `Backspace` | Delete last letter |
| `Enter` | Submit guess |
| `Ctrl+R` | Start new game |
| `Ctrl+Q` | Quit game |

## 🎨 Screenshots

```
┌───────────────────────────────────────────┐
│  W   O   R   D   L   E                    │
│                                           │
│  ┏━━┓ ┏━━┓ ┏━━┓ ┏━━┓ ┏━━┓               │
│  ┃ H ┃ ┃ E ┃ ┃ L ┃ ┃ L ┃ ┃ O ┃  Row 1    │
│  ┗━━┛ ┗━━┛ ┗━━┛ ┗━━┛ ┗━━┛               │
│                                           │
│  ┏━━┓ ┏━━┓ ┏━━┓ ┏━━┓ ┏━━┓               │
│  ┃ W ┃ ┃ O ┃ ┃ R ┃ ┃ L ┃ ┃ D ┃  Row 2    │
│  ┗━━┛ ┗━━┛ ┗━━┛ ┗━━┛ ┗━━┛               │
│                                           │
│         ... (4 more rows)                 │
│                                           │
│  Keyboard with color feedback             │
└───────────────────────────────────────────┘
```

## 🏗️ Project Structure

```
wordle_cli/
├── src/
│   └── wordle_cli/
│       ├── __main__.py          # Entry point
│       ├── app.py                # Main application
│       ├── domain/               # Game logic
│       │   ├── game_engine.py
│       │   ├── evaluator.py
│       │   └── models.py
│       ├── adapters/             # External interfaces
│       │   └── word_repository.py
│       ├── widgets/              # UI components
│       │   ├── grid.py
│       │   ├── cell.py
│       │   └── keyboard.py
│       └── styles/
│           └── app.tcss          # Textual CSS
├── tests/                        # Unit tests
├── words.py                      # Word dictionary
├── pyproject.toml               # Project config
└── README.md
```

## 🧪 Running Tests

Run the test suite:

```bash
pytest tests/
```

All 29 domain tests should pass:
- Word repository tests
- Guess evaluation tests (including duplicate letter handling)
- Game engine tests (win/loss conditions, state management)

## 🛠️ Technical Details

- **Framework**: [Textual](https://textual.textualize.io/) - Modern TUI framework
- **Architecture**: Clean Architecture with domain-driven design
- **Color Scheme**: Official Wordle color palette
  - Correct: `#6aaa64` (green)
  - Present: `#c9b458` (yellow)
  - Absent: `#787c7e` (gray)

## 🎓 Learning Points

This project demonstrates:
- ✅ Clean Architecture principles
- ✅ Domain-driven design
- ✅ Reactive UI patterns
- ✅ Test-driven development
- ✅ Python type hints
- ✅ Modern terminal UI with Textual

## 📝 License

MIT License - Feel free to use this project for learning or fun!

## 🙏 Acknowledgments

- Inspired by the original [Wordle](https://www.nytimes.com/games/wordle) by Josh Wardle
- Built with [Textual](https://textual.textualize.io/) by Textualize.io
- Word list from common English 5-letter words

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

**Enjoy playing Wordle in your terminal!** 🎉

For questions or feedback, please open an issue on GitHub.
