#!/usr/bin/env python3
"""Four in a Line - Main Entry Point"""

import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from four_in_line.board import Board
from four_in_line.player import Player
from four_in_line.ai import AI
from four_in_line.game import Game


# Score tracking across games
SCORES = {'player1': 0, 'player2': 0, 'draws': 0}


def clear_screen():
    """Clear terminal screen - cross platform."""
    os.system('cls' if os.name == 'nt' else 'clear')


def animate_drop(board, col, piece, delay=0.05):
    """Animate piece dropping into column."""
    # Find target row
    target_row = -1
    for row in range(board.ROWS - 1, -1, -1):
        if board.grid[row][col] == board.EMPTY:
            target_row = row
            break
    
    if target_row == -1:
        return  # Column full
    
    # Animate falling
    temp_grid = [row[:] for row in board.grid]  # Copy current state
    
    for row in range(target_row + 1):
        # Clear and redraw
        clear_screen()
        
        # Create animation frame
        frame = [r[:] for r in temp_grid]
        if row > 0:
            frame[row - 1][col] = board.EMPTY  # Clear previous position
        frame[row][col] = piece  # Current position
        
        # Print animated board
        print("  " + " ".join(str(i + 1) for i in range(board.COLS)))
        print(" ┌" + "─┬" * (board.COLS - 1) + "─┐")
        
        for r in range(board.ROWS):
            row_str = " │"
            for c in range(board.COLS):
                p = frame[r][c]
                if p == board.EMPTY:
                    row_str += "  │"
                elif p == board.PLAYER1:
                    row_str += "\033[91m●\033[0m │"  # Red
                else:
                    row_str += "\033[93m●\033[0m │"  # Yellow
            print(row_str)
            if r < board.ROWS - 1:
                print(" ├" + "─┼" * (board.COLS - 1) + "─┤")
        
        print(" └" + "─┴" * (board.COLS - 1) + "─┘")
        time.sleep(delay)
    
    # Final state
    board.grid[target_row][col] = piece


def show_menu():
    """Display main menu with enhanced styling."""
    clear_screen()
    print("\n" + "=" * 50)
    print("    🔴 FOUR IN A LINE 🟡".center(50))
    print("=" * 50)
    print()
    print("    1. New Game (Human vs Human)")
    print("    2. New Game (Human vs AI)")
    print("    3. New Game (AI vs AI)")
    print("    4. Load Game")
    print("    5. Instructions")
    print("    6. View Scoreboard")
    print("    7. Quit")
    print()
    print("-" * 50)
    
    # Show current series score if any games played
    total = sum(SCORES.values())
    if total > 0:
        print(f"    Series Score: Red {SCORES['player1']} - {SCORES['player2']} Yellow | Draws: {SCORES['draws']}")
    print("=" * 50)


def show_instructions():
    """Display game rules with formatting."""
    clear_screen()
    print("\n" + "=" * 50)
    print("    HOW TO PLAY".center(50))
    print("=" * 50)
    print()
    print("    Four in a Line (Connect Four):")
    print()
    print("    • Two players take turns dropping pieces")
    print("    • Pieces fall to the lowest available space")
    print("    • First to get FOUR in a row wins!")
    print("    • Lines can be horizontal, vertical, or diagonal")
    print()
    print("    Controls:")
    print("    • Enter column number (1-7) to drop piece")
    print("    • Enter 'q' to quit current game")
    print("    • Turn on animations for visual effect")
    print()
    print("    Colors: 🔴 Red (Player 1)  🟡 Yellow (Player 2)")
    print("=" * 50)
    input("\n    Press Enter to continue...")


def show_scoreboard():
    """Display current series scores."""
    clear_screen()
    print("\n" + "=" * 50)
    print("    SERIES SCOREBOARD".center(50))
    print("=" * 50)
    print()
    print(f"    🔴 Red Wins:    {SCORES['player1']}")
    print(f"    🟡 Yellow Wins: {SCORES['player2']}")
    print(f"    🤝 Draws:       {SCORES['draws']}")
    print()
    total = sum(SCORES.values())
    if total > 0:
        print(f"    Total Games: {total}")
        p1_pct = (SCORES['player1'] / total) * 100
        p2_pct = (SCORES['player2'] / total) * 100
        draw_pct = (SCORES['draws'] / total) * 100
        print(f"    Red Win %:   {p1_pct:.1f}%")
        print(f"    Yellow Win %: {p2_pct:.1f}%")
        print(f"    Draw %:       {draw_pct:.1f}%")
    print("=" * 50)
    input("\n    Press Enter to continue...")


def select_ai_difficulty():
    """Get AI difficulty level."""
    print("\n    Select difficulty:")
    print("    1. Easy (random moves)")
    print("    2. Medium (blocks wins, prefers center)")
    print("    3. Hard (minimax with alpha-beta pruning)")
    
    while True:
        choice = input("    Choice (1-3): ").strip()
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'medium'
        elif choice == '3':
            return 'hard'
        else:
            print("    Invalid choice. Try again.")


def ask_animation():
    """Ask if user wants drop animations."""
    print("\n    Enable drop animations?")
    print("    1. Yes (slower but visual)")
    print("    2. No (faster gameplay)")
    
    while True:
        choice = input("    Choice (1-2): ").strip()
        if choice == '1':
            return True
        elif choice == '2':
            return False
        else:
            print("    Invalid choice. Try again.")


def list_saved_games():
    """List available save files with metadata."""
    saves = Game.list_saved_games()
    if not saves:
        return []
    return [s for s in saves if not s.get('corrupted')]


def update_scores(winner, player1_name, player2_name):
    """Update series scores after game."""
    if winner is None:
        SCORES['draws'] += 1
    elif 'Red' in winner or player1_name in winner:
        SCORES['player1'] += 1
    else:
        SCORES['player2'] += 1


def main():
    """Main game loop."""
    global SCORES
    
    while True:
        show_menu()
        
        choice = input("\n    Enter choice (1-7): ").strip()
        
        if choice == '1':
            # Human vs Human
            clear_screen()
            print("\n    " + "=" * 50)
            print("    HUMAN vs HUMAN".center(50))
            print("    " + "=" * 50)
            
            name1 = input("    Player 1 name (🔴 Red): ").strip() or "Player 1"
            name2 = input("    Player 2 name (🟡 Yellow): ").strip() or "Player 2"
            animate = ask_animation()
            
            p1 = Player(name1, 1)
            p2 = Player(name2, 2)
            game = Game(p1, p2)
            
            # Override play_turn to add animation
            if animate:
                original_play = game.play_turn
                def animated_turn():
                    game.board.display()
                    print(f"\n    {game.current_player}'s turn")
                    col = game.current_player.get_move(game.board)
                    if col is None:
                        return False
                    animate_drop(game.board, col, game.current_player.piece)
                    # Continue with normal win checking...
                    return original_play()
                game.play_turn = animated_turn
            
            game.play()
            update_scores(game.winner, name1, name2)
            input("\n    Press Enter to continue...")
            
        elif choice == '2':
            # Human vs AI
            clear_screen()
            print("\n    " + "=" * 50)
            print("    HUMAN vs AI".center(50))
            print("    " + "=" * 50)
            
            name = input("    Your name: ").strip() or "Player"
            difficulty = select_ai_difficulty()
            animate = ask_animation()
            
            p1 = Player(name, 1)
            p2 = AI(2, difficulty)
            p2.name = f"AI ({difficulty})"
            game = Game(p1, p2, auto_save=True)
            game.play()
            update_scores(game.winner, name, p2.name)
            input("\n    Press Enter to continue...")
            
        elif choice == '3':
            # AI vs AI
            clear_screen()
            print("\n    " + "=" * 50)
            print("    AI vs AI BATTLE".center(50))
            print("    " + "=" * 50)
            
            diff1 = select_ai_difficulty()
            diff2 = select_ai_difficulty()
            
            p1 = AI(1, diff1)
            p1.name = f"AI-1 ({diff1})"
            p2 = AI(2, diff2)
            p2.name = f"AI-2 ({diff2})"
            
            game = Game(p1, p2)
            game.play()
            update_scores(game.winner, p1.name, p2.name)
            input("\n    Press Enter to continue...")
            
        elif choice == '4':
            # Load game
            saves = list_saved_games()
            if not saves:
                print("\n    No saved games found.")
                input("    Press Enter to continue...")
                continue
            
            clear_screen()
            print("\n    " + "=" * 50)
            print("    LOAD GAME".center(50))
            print("    " + "=" * 50)
            
            for i, save in enumerate(saves[:10], 1):  # Show top 10
                status = "✓" if not save.get('corrupted') else "✗"
                moves = save.get('move_count', '?')
                players = ', '.join(save.get('players', ['Unknown']))
                print(f"    {i}. {save['filename'][:30]:30} | Moves: {moves:2} | {players}")
            
            print()
            try:
                idx = int(input("    Select game number: ")) - 1
                if 0 <= idx < len(saves):
                    game = Game.load(saves[idx]['filepath'])
                    print(f"\n    Loaded game: {saves[idx]['filename']}")
                    game.play()
                else:
                    print("    Invalid selection.")
            except (ValueError, FileNotFoundError, Exception) as e:
                print(f"    Error loading game: {e}")
            
            input("\n    Press Enter to continue...")
            
        elif choice == '5':
            show_instructions()
            
        elif choice == '6':
            show_scoreboard()
            
        elif choice == '7':
            print("\n    Thanks for playing!")
            print(f"    Final Score - Red: {SCORES['player1']} Yellow: {SCORES['player2']} Draws: {SCORES['draws']}")
            break
            
        else:
            print("    Invalid choice. Try again.")
            input("    Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n    Game interrupted. Goodbye!")
        print(f"    Final Score - Red: {SCORES['player1']} Yellow: {SCORES['player2']} Draws: {SCORES['draws']}")
        sys.exit(0)