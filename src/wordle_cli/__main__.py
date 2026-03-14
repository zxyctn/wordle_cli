"""Entry point for Wordle CLI application."""

from wordle_cli.app import WordleApp


def main() -> None:
    """Run the Wordle CLI application."""
    app = WordleApp()
    app.run()


if __name__ == "__main__":
    main()
