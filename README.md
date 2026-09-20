# 581-P1-Minesweeper

## Board System

The board is defined in `board.py` and provides the shared data model that every other module (mines, reveal, flags, display) reads from and writes to. It is intentionally state-only: no mine placement, no user input, no win/loss logic.

The module exports two classes and one constant:

- `Cell` - state for a single square.
- `Board` - the 10x10 grid of `Cell`s plus accessor methods.
- `COLUMN_LETTERS` - the string `"ABCDEFGHIJ"` used for column labels.

### Cell

Each `Cell` tracks the four state flags called out in the spec:

- `is_mine` - whether the cell hides a mine.
- `is_covered` - whether the cell is still hidden from the player.
- `is_flagged` - whether the player has flagged it.
- `adjacent_mines` - number of neighboring mines (0-8), set by mine-placement logic.

Every cell starts covered, unflagged, non-mine, with `adjacent_mines = 0`.

### Board

Create a fresh 10x10 board with no arguments:

```python
board = Board()
```

The board addresses cells using **0-indexed rows** (`0`-`9`, matching Python) and **letter columns** (`"A"`-`"J"`, matching the player-facing labels). If the UI receives input like `D5`, it should convert to:

```python
row = 4      # 5 - 1
col = "D"
board.get_cell(row, col)
```

Column letters are case-insensitive on input; `get_cell(0, "a")` and `get_cell(0, "A")` return the same cell.

### Methods

Position validation and column conversion:
- `is_valid_position(row, col_index)` - True if a 0-indexed `(row, col_index)` is on the board. `col_index` here is an integer, used internally after a letter has been converted.
- `col_letter_to_index(letter)` - Convert `"A"`-`"J"` to `0`-`9`. Raises `ValueError` on anything else.
- `col_index_to_letter(index)` - Convert `0`-`9` back to `"A"`-`"J"`.

Cell access:
- `get_cell(row, col)` - Return the `Cell` at `(row, col)`. Raises `ValueError` on a bad column letter, `IndexError` on a bad row.
- `set_cell(row, col, *, is_mine=None, is_covered=None, is_flagged=None, adjacent_mines=None)` - Update only the fields explicitly passed as keyword arguments; everything else is left untouched. This lets other modules change one attribute at a time without clobbering the rest.

Geometry:
- `neighbors(row, col)` - Return up to eight `(row, col_letter)` neighbor positions. Corners return 3, edges 5, interior cells 8.

Iteration helpers:
- `iter_positions()` - Yield every `(row, col_letter)` on the board (100 tuples).
- `iter_cells()` - Yield every `(row, col_letter, cell)` triple; the `cell` is the live reference, so mutations persist.

Development helper:
- `print_board()` - Print the whole board to stdout using single-character glyphs (`X` covered, `F` flagged, `O` uncovered-zero, `1`-`8` for adjacent-mine counts, `*` for an uncovered mine). Used for debugging; the real game uses `display.render` instead.


## Flagging System

Flagging is handled by the `FlagManager` class in `flags.py`.

Create it using the current board and the user-selected number of mines:

```python
flags = FlagManager(board, mine_count)
```

`mine_count` must be the same number used when placing mines. If the user chooses 15 mines, the player gets 15 flags.

### Functions
- `place_flag(row, col)` - Flags a covered cell and removes one available flag.
- `remove_flag(row, col)` - Unflags a cell and gives one flag back.
- `get_flags_remaining()` - Returns the number of flags still available.

The board uses **0-indexed rows** and **letter columns**. For example, user input `D5` must be converted to:

```python
row = 4
col = "D"
flags.place_flag(row, col)
```

The UI is responsible for converting user input like `D5`. The reveal system must check `cell.is_flagged` and not reveal the cell if it is `True`.



## Game Logic

The `game.py` module manages the overall game lifecycle, rule enforcement, and state transitions for Minesweeper. It acts as the central coordinator connecting the board data structure (`Board`), mine placement (`MineManager`), flagging mechanics (`FlagManager`), and uncovering logic (`reveal`).

### Key Responsibilities & Features

- **Game State Tracking**: Maintains and updates the internal state of the game (`PLAYING`, `VICTORY`, or `LOSS`).
- **First-Click Safety**: Ensures the player never hits a mine on their initial turn by triggering lazy mine generation via `MineManager` on the first reveal action.
- **Win & Loss Detection**:
  - **Win Condition**: Evaluates whether all non-mine cells on the board have been uncovered.
  - **Loss Condition**: Triggers game over when a mine cell is revealed.
- **Mine Uncovering on Defeat**: Automatically uncovers all hidden mines across the board when a loss occurs.
- **Component Coordination**: Directs user inputs/commands (`reveal`, `flag`, `unflag`) to their respective manager modules without directly handling terminal I/O or printing.

---

### Class Architecture

#### Attributes
- `board` (`Board`): The 10x10 grid instance.
- `mine_manager` (`MineManager`): Handles random mine generation and adjacent mine counts.
- `flag_manager` (`Optional[FlagManager]`): Handles flag placement limits and flag state updates.
- `state` (`str`): Current game status (`"PLAYING"`, `"VICTORY"`, or `"LOSS"`).
- `first_move` (`bool`): Flag tracking whether the next move is the initial click.

#### Primary Methods
- `process_move(command: str, target: Tuple[int, str], reveal_func=None) -> None`:  
  Processes user actions (`'reveal'`, `'flag'`, `'unflag'`), updates flag/mine managers, and evaluates post-move game state.
- `check_win() -> bool`:  
  Checks if all non-mine cells are uncovered. Returns `True` if victory conditions are met.
- `end_game(won: bool) -> None`:  
  Sets the state to `"VICTORY"` or `"LOSS"`. If `won=False`, executes `_reveal_all_mines()`.
- `_reveal_all_mines() -> None`:  
  Internal helper to set `is_covered = False` for all cells where `is_mine == True`.
