"""Entry point for the Minesweeper game.

The board data model lives in ``board.py``. Mine placement, user input,
rendering, and win/loss logic are being implemented in sibling modules by
other teammates and will be wired in here once they land.
"""

from board import Board


def main() -> None:
    board = Board()
    # Placeholder: the full game loop lives in other modules once merged.
    # Touching the board here just confirms the data model imports cleanly.


if __name__ == "__main__":
    main()
