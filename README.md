# Four in Line

Two terminal-based Connect Four implementations in Python, each in its own directory.

---

## [`1/`](./1) — Four in a Line 🔴🟡

A full-featured Connect Four game with AI opponents, save/load, and a polished UI.

- **Game modes:** Human vs Human, Human vs AI, AI vs AI
- **AI:** Easy (random), Medium (win/block/center), Hard (minimax + alpha-beta, depth 4)
- **UI:** ANSI red/yellow pieces, drop animations, series score tracking, Unicode box-drawing board
- **Save/load:** JSON files with atomic writes, auto-save every 5 moves, corruption-resistant
- **Tests:** 7 test files covering board, AI, game, player, save/load, integration, and UI
- **Run:** `python 1/main.py`

---

## [`2/`](./2) — Connect Four ❌⭕

A simple two-player-only Connect Four game with a basic text interface.

- **Gameplay:** Two players take turns (Player 1 = X, Player 2 = O)
- **UI:** Simple pipe-and-dash board with column numbers 0–6
- **Engine:** Compact single-class engine with win/draw detection
- **Tests:** One test file
- **Run:** `python 2/main.py`

---

## Comparison

| Feature | `1/` | `2/` |
|---------|------|------|
| AI opponents | ✅ (3 difficulties) | ❌ |
| Save / Load | ✅ | ❌ |
| Drop animation | ✅ | ❌ |
| Score tracking | ✅ | ❌ |
| Colored pieces | ✅ (ANSI) | ❌ (plain X/O) |
| Code size | ~700 LOC | ~100 LOC |
| Test files | 7 | 1 |

## Requirements

- Python 3.7+
- Terminal with Unicode support
- ANSI color support recommended for `1/`
