#!/usr/bin/env python3
"""Quick test of game functionality without interactive input."""

import sys
import os

# Setup path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import using package structure
from four_in_line.board import Board
from four_in_line.ai import AI
from four_in_line.game import Game

def test_ai_game():
    """Run quick AI vs AI game."""
    print("Testing AI vs AI game...")
    
    # Create AIs
    ai1 = AI(1, 'easy')
    ai1.name = "AI-Easy"
    ai2 = AI(2, 'medium')
    ai2.name = "AI-Medium"
    
    # Create game
    game = Game(ai1, ai2)
    
    # Simulate moves
    max_moves = 15
    move = 0
    
    while not game.game_over and move < max_moves:
        col = game.current_player.get_move(game.board)
        if col is None:
            break
            
        row = game.board.drop_piece(col, game.current_player.piece)
        if row == -1:
            print(f"Invalid move by {game.current_player}")
            break
            
        print(f"Move {move + 1}: {game.current_player.name} drops in column {col + 1}")
        
        if game.board.check_win(game.current_player.piece):
            print(f"\n{game.current_player.name} WINS!")
            game.board.display()
            break
            
        if game.board.is_full():
            print("\nDRAW!")
            break
            
        game.switch_player()
        move += 1
    
    if move >= max_moves:
        print(f"\nGame stopped after {max_moves} moves (test limit)")
        game.board.display()
    
    return True

def test_board_display():
    """Test board rendering."""
    print("\nTesting board display...")
    board = Board()
    
    # Add some pieces
    board.drop_piece(3, 1)  # Red in center
    board.drop_piece(2, 2)  # Yellow
    board.drop_piece(3, 1)  # Red on top
    
    board.display()
    return True

def test_win_detection():
    """Test all win types."""
    print("\nTesting win detection...")
    
    # Horizontal
    b1 = Board()
    for c in range(4):
        b1.drop_piece(c, 1)
    assert b1.check_win(1), "Horizontal win failed"
    print("✓ Horizontal win detected")
    
    # Vertical
    b2 = Board()
    for _ in range(4):
        b2.drop_piece(0, 1)
    assert b2.check_win(1), "Vertical win failed"
    print("✓ Vertical win detected")
    
    # Diagonal
    b3 = Board()
    b3.grid[5][0] = 1
    b3.grid[4][1] = 1
    b3.grid[3][2] = 1
    b3.grid[2][3] = 1
    assert b3.check_win(1), "Diagonal win failed"
    print("✓ Diagonal win detected")
    
    return True

def test_save_load():
    """Test save and load functionality."""
    print("\nTesting save/load...")
    
    ai1 = AI(1, 'easy')
    ai2 = AI(2, 'easy')
    game = Game(ai1, ai2)
    
    # Make a few moves
    for _ in range(3):
        col = game.current_player.get_move(game.board)
        game.board.drop_piece(col, game.current_player.piece)
        game.switch_player()
    
    # Save
    filepath = game.save("test_save.json")
    print(f"Saved to {filepath}")
    
    # Load
    loaded = Game.load(filepath)
    print(f"Loaded game with {loaded.move_count} moves")
    
    # Cleanup
    if os.path.exists(filepath):
        os.remove(filepath)
        print("Cleaned up test file")
    
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("FOUR IN A LINE - Automated Tests")
    print("=" * 50)
    
    test_board_display()
    test_win_detection()
    test_ai_game()
    test_save_load()
    
    print("\n" + "=" * 50)
    print("All tests passed!")
    print("=" * 50)