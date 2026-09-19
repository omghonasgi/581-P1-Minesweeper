"""
Author: Jal Maru
Date: 2026-09-16
Module: game.py
Outside Sources: Gemini Flash
Description: Game logic controller for Minesweeper. Manages game lifecycle states
    (PLAYING, VICTORY, LOSS), win/loss evaluation, initial setup, and end-game triggers.
"""

from typing import Tuple, Optional
from board import Board
from mines import MineManager
from flags import FlagManager


class Game:
    # manages overall Minesweeper game state and rule evaluations

    def __init__(self) -> None:
        self.board = Board()
        self.mine_manager = MineManager(self.board)
        self.flag_manager: Optional[FlagManager] = None
        self.state: str = "PLAYING"  # valid states are "PLAYING", "VICTORY", "LOSS"
        self.first_move: bool = True

    def process_move(
        self,
        command: str,
        target: Tuple[int, str],
        mine_count: int,
        reveal_func=None,
    ) -> None:
        """processes a move command from the UI and evaluates state updates
        :param command: action string ('reveal', 'flag', 'unflag')
        :param target: row and column tuple
        :param mine_count: user-selected mine count (10-20); used only on the
            first reveal to seed the minefield and the flag counter
        :param reveal_func: Reference to board.reveal implementation
        """
        if self.state != "PLAYING":
            return

        row, col = target
        cell = self.board.get_cell(row, col)

        if command == "reveal":
            if cell.is_flagged:
                return

            # Ensure safe first click by delaying mine generation
            if self.first_move:
                self.mine_manager.place_mines((row, col), mine_count)
                self.mine_manager.calculate_numbers()
                self.flag_manager = FlagManager(self.board, mine_count)
                self.first_move = False

            # Delegate cell uncovering to Marcos's reveal function/method
            if reveal_func:
                reveal_func(row, col)
            else:
                self.board.set_cell(row, col, is_covered=False)

            # Evaluate state transitions after the move
            if cell.is_mine:
                self.end_game(won=False)
            elif self.check_win():
                self.end_game(won=True)

        elif command == "flag" and self.flag_manager:
            self.flag_manager.place_flag(row, col)

        elif command == "unflag" and self.flag_manager:
            self.flag_manager.remove_flag(row, col)

    def check_win(self) -> bool:
        """Return True if every non-mine cell on the board has been revealed."""
        for _, _, cell in self.board.iter_cells():
            if not cell.is_mine and cell.is_covered:
                return False
        return True

    def end_game(self, won: bool) -> None:
        """Updates internal game state and reveals all hidden mines on loss."""
        if won:
            self.state = "VICTORY"
        else:
            self.state = "LOSS"
            self._reveal_all_mines()

    def _reveal_all_mines(self) -> None:
        """Uncovers all mine locations on the board following a loss."""
        for row, col, cell in self.board.iter_cells():
            if cell.is_mine:
                self.board.set_cell(row, col, is_covered=False)
