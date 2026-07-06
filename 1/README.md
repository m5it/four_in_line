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

## Quick Start

```bash
# Run the game
python main.py
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
1/
├── __init__.py    # Package initialization
├── board.py       # 7x6 grid, win detection
├── player.py      # Human player input
├── ai.py          # AI with 3 difficulty levels
├── game.py        # Game loop, save/load
├── main.py        # Entry point, menus, UI
├── test_*.py      # Test suite (7 test files)
└── README.md      # This file
```

## Testing

```bash
python board.py          # Board tests
python test_ai.py        # AI tests
python test_game.py      # Game tests
python test_player.py    # Player tests
python test_save_load.py # Save/load tests
python test_integration.py # Integration tests
python test_ui.py        # UI tests
python test_game_flows.py # Game flow tests
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
  "board": [[0, 0, ...], ...],
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
