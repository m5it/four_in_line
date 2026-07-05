# Four in a Line 🔴🟡

A complete terminal-based Connect Four game in Python with AI opponents, save/load functionality, and polished UI.

## Features

### Game Modes
- **Human vs Human**: Two-player local gameplay
- **Human vs AI**: Challenge three difficulty levels
- **AI vs AI**: Watch computer players battle

### AI Difficulties
| Level | Strategy |
|-------|----------|
| **Easy** | Random valid moves |
| **Medium** | Blocks wins, takes winning moves, prefers center columns |
| **Hard** | Minimax with alpha-beta pruning, depth-4 lookahead, position evaluation |

### UI Features
- 🔴 **Red** and 🟡 **Yellow** pieces with ANSI colors
- Drop animation option (visual effect)
- Clear screen between turns
- Series score tracking (best of games)
- Column headers (1-7)

### Persistence
- Save games to JSON
- Load saved games with metadata
- Auto-save every 5 moves
- Corruption-resistant (atomic writes, validation)

## Installation

```bash
git clone <repository>
cd four_in_line
python -m four_in_line.main
```

## Quick Start

```bash
# Run the game
python -m four_in_line.main

# Or directly
python four_in_line/main.py
```

## How to Play

1. Select game mode from the menu (1-7)
2. Enter column number **1-7** to drop piece
3. First to connect **four** horizontally, vertically, or diagonally wins!
4. Enter **'q'** to quit current game (auto-saves if enabled)

## Controls

| Input | Action |
|-------|--------|
| 1-7 | Drop piece in column |
| q | Quit current game |
| Enter | Continue after game |

## Project Structure

```
four_in_line/
├── __init__.py          # Package initialization
├── board.py             # 7x6 grid, win detection
├── player.py            # Human player input
├── ai.py                # AI with 3 difficulty levels
├── game.py              # Game loop, save/load
├── main.py              # Entry point, menus, UI
└── README.md            # This file
```

## Testing

Run all tests:
```bash
# Board tests
python four_in_line/board.py

# AI tests
python four_in_line/test_ai.py

# Save/load tests  
python four_in_line/test_save_load.py

# Integration tests
python four_in_line/test_integration.py
```

## Technical Details

### Win Detection
- Horizontal, vertical, diagonal (both slopes)
- Optimized scanning with early termination

### AI Hard Algorithm
```
Minimax with Alpha-Beta Pruning
├── Depth: 4 levels
├── Evaluation: Center control + threats
├── Ordering: Center columns first (better pruning)
└── Scoring: +100000 win, -100000 loss, +100 threat, +10 potential
```

### Save Format (JSON)
```json
{
  "version": "1.0",
  "board": [[0, 0, ...], ...],  // 6x7 grid
  "current_player": 0,
  "move_count": 15,
  "move_history": [...],
  "players": [{"name": "...", "type": "human|ai", "difficulty": "..."}]
}
```

## Requirements

- Python 3.7+
- Terminal with Unicode support (for box-drawing characters)
- ANSI color support recommended (for red/yellow pieces)

## Cross-Platform

Tested on:
- Linux (primary)
- macOS
- Windows (with ANSI support)

## License

MIT License - Free to use, modify, distribute