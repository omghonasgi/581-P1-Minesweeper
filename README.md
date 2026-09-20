# 581-P1-Minesweeper

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
