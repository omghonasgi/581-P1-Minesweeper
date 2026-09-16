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