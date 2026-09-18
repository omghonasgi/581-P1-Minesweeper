"""Entry point for the Minesweeper game.

The board data model lives in ``board.py``. Mine placement, user input,
rendering, and win/loss logic are being implemented in sibling modules by
other teammates and will be wired in here once they land.
"""

from board import Board
from mines import MineManager


def main() -> None:
    board = Board()
    # Placeholder: the full game loop lives in other modules once merged.
    # Touching the board here just confirms the data model imports cleanly.
    mine_manager = MineManager(board)
    
    # mine_count = ?  Store users mine count input, which must be from 10 through 20.
    # first_click = ?  Will hold the first click position (row, col) to avoid placing mines there and adjacent cells.
    # mine_manager.place_mines(first_click, mine_count)
    # mine_manager.calculate_numbers()
    
    # reveal function called here


if __name__ == "__main__":
    main()
