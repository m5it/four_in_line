# Connect Four ❌⭕

A simple terminal-based two-player Connect Four game in Python.

## Features

- **Two-player local gameplay** (Player 1 = X, Player 2 = O)
- **6×7 board** with simple text-based display
- **Win detection** — horizontal, vertical, and diagonal (both slopes)
- **Draw detection** — board full with no winner
- **Column validation** — prevents invalid column numbers and full columns

## Quick Start

```bash
python main.py
```

## How to Play

1. Players take turns choosing a column (**0-6**) to drop their piece
2. Pieces fall to the lowest available space in the column
3. First to connect **four** in a row horizontally, vertically, or diagonally wins
4. If the board fills with no winner, it's a draw

## Controls

| Input | Action |
|-------|--------|
| 0-6 | Drop piece in column |

## Project Structure

```
2/
├── engine.py    # Game logic: board, drops, win/draw checks, player switching
├── ui.py        # Terminal UI: board display, input, messages
├── main.py      # Entry point and game loop
├── plans/       # Game plan / state files
└── README.md    # This file
```

## Testing

```bash
python test_game.py
```

## Requirements

- Python 3.7+

## Technical Details

### Win Detection
Scans every cell; for each non-empty cell, checks four directions (right, down, down-right, up-right) for a matching run of 4.

### Board Display
```
  0 1 2 3 4 5 6
---------------
|.|.|.|.|.|.|.|
|.|.|.|.|.|.|.|
|.|.|.|X|.|.|.|
|.|.|O|X|.|.|.|
|.|O|X|O|.|.|.|
|O|X|O|X|O|.|.|
---------------
```
