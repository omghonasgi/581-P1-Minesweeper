"""
Author: Axel Bengoa
Date: 2026-09-16
Module: test_terminal_ui.py
Outside sources: Claude Code.
Description: Unit tests for display.py and input_handler.py.
    Run with: python -m unittest test_terminal_ui
Inputs: none. 
Outputs: pass/fail report.
"""

import unittest
from unittest.mock import patch

from board import Board
from display import cell_glyph, COVERED, FLAGGED, MINE, EMPTY
from input_handler import parse_cell, parse_action, get_mine_count, get_move


class TestParseCell(unittest.TestCase):
    def test_valid_cells(self):
        self.assertEqual(parse_cell("A1"), (0, "A"))
        self.assertEqual(parse_cell("d5"), (4, "D"))
        self.assertEqual(parse_cell(" J10 "), (9, "J"))
        self.assertEqual(parse_cell("c 3"), (2, "C"))

    def test_invalid_cells(self):
        for bad in ["", "A", "5", "K1", "A0", "A11", "A-1", "5D", "AA", "A5.0", "!!"]:
            self.assertIsNone(parse_cell(bad), bad)


class TestParseAction(unittest.TestCase):
    def test_actions(self):
        self.assertEqual(parse_action("1"), "reveal")
        self.assertEqual(parse_action(" FLAG "), "flag")
        self.assertEqual(parse_action("3"), "unflag")
        self.assertEqual(parse_action("q"), "quit")
        self.assertIsNone(parse_action("5"))
        self.assertIsNone(parse_action(""))


class TestPrompts(unittest.TestCase):
    @patch("builtins.input", side_effect=["abc", "9", "21", "15"])
    def test_mine_count_reprompts(self, _):
        self.assertEqual(get_mine_count(), 15)

    @patch("builtins.input", side_effect=["7", "2", "Z9", "b", "1", "B2"])
    def test_move_with_bad_input_and_back(self, _):
        self.assertEqual(get_move(), ("reveal", 1, "B"))

    @patch("builtins.input", side_effect=EOFError)
    def test_ctrl_d_quits_cleanly(self, _):
        self.assertEqual(get_move(), ("quit", None, None))


class TestGlyphs(unittest.TestCase):
    def test_each_state(self):
        b = Board()
        self.assertEqual(cell_glyph(b.get_cell(0, "A")), COVERED)
        b.set_cell(0, "B", is_flagged=True)
        self.assertEqual(cell_glyph(b.get_cell(0, "B")), FLAGGED)
        b.set_cell(0, "C", is_covered=False)
        self.assertEqual(cell_glyph(b.get_cell(0, "C")), EMPTY)
        b.set_cell(0, "D", is_covered=False, adjacent_mines=3)
        self.assertEqual(cell_glyph(b.get_cell(0, "D")), "3")
        b.set_cell(0, "E", is_covered=False, is_mine=True)
        self.assertEqual(cell_glyph(b.get_cell(0, "E")), MINE)


if __name__ == "__main__":
    unittest.main()
