"""Entry point for the Minesweeper game.

Wires together the game controller, reveal cascade, input, and display
modules into a single terminal game loop.
"""

from display import render, render_message
from game import Game
from input_handler import get_mine_count, get_move
from reveal import RevealManager


# Map Game's internal state names to the user-facing status strings.
STATUS_LABEL = {
    "PLAYING": "Playing",
    "VICTORY": "Victory",
    "LOSS": "Game Over: Loss",
}


def main() -> None:
    print("Welcome to Minesweeper!")

    mine_count = get_mine_count()
    if mine_count is None:
        # Player hit Ctrl+C / Ctrl+D at the mine-count prompt.
        print("Goodbye!")
        return

    game = Game()

    # Game places mines itself on the first reveal. We still want the
    # cascade uncovering that RevealManager provides, so we pass its
    # reveal method as the reveal_func and flip its own first-reveal
    # flag so it doesn't try to place a second set of mines on top.
    reveal_manager = RevealManager(game.board, mine_count, game.mine_manager)

    def reveal_func(row: int, col: str) -> None:
        reveal_manager.first_reveal_done = True
        reveal_manager.reveal(row, col)

    while game.state == "PLAYING":
        flags_left = (
            game.flag_manager.get_flags_remaining()
            if game.flag_manager is not None
            else mine_count
        )
        render(game.board, flags_left, STATUS_LABEL[game.state])

        action, row, col = get_move()
        if action == "quit":
            render_message("Thanks for playing!")
            return

        game.process_move(action, (row, col), mine_count, reveal_func=reveal_func)

    # Final board + terminal status.
    flags_left = (
        game.flag_manager.get_flags_remaining()
        if game.flag_manager is not None
        else mine_count
    )
    render(game.board, flags_left, STATUS_LABEL[game.state])
    if game.state == "VICTORY":
        render_message("You won! All safe cells cleared.")
    else:
        render_message("You hit a mine. Better luck next time!")


if __name__ == "__main__":
    main()
