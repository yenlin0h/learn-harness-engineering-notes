"""Entry point for the 2D retro tile map editor.

Run with:
    python main.py
"""

from editor.app import Editor


def main():
    editor = Editor()
    editor.run()


if __name__ == "__main__":
    main()
