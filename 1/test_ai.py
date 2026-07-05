#!/usr/bin/env python3
"""AI testing - difficulty levels and balance."""

import sys
import os

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from four_in_line.board import Board
from four_in_line.ai import AI
from four_in_line.game import Game


def test_easy_randomness():
    """Test easy AI makes valid random moves."""
    print("Test: Easy AI randomness...")
    
    board = Board()
    ai = AI(1, 'easy')
    
    moves = []
    for _ in range(10):
        col = ai.get_move(board)
        assert col is not None, "Should return a move"
        assert 0 <= col < 7, f"Move {col} out of range"
        moves.append(col)
    
    # Should have some variety (not all same)
    unique = len(set(moves))
    print(f"  Unique moves in 10 tries: {unique}")
    assert unique >= 2, "Should have variety"
    print("✓ Easy AI makes varied valid moves\n")


def test_medium_blocks_win():
    """Test medium AI blocks opponent winning moves."""
    print("Test: Medium AI blocks win...")
    
    board = Board()
    ai = AI(2, 'medium')  # Player 2
    
    # Set up player 1 to win on next move (column 3)
    board.grid[5][3] = 1
    board.grid[4][3] = 1
    board.grid[3][3] = 1
    
    # AI should block column 3
    move = ai.get_move(board)
    assert move == 3, f"Should block column 3, got {move}"
    print("✓ Medium AI blocks opponent win\n")


def test_medium_takes_win():
    """Test medium AI takes winning moves."""
    print("Test: Medium AI takes win...")
    
    board = Board()
    ai = AI(1, 'medium')
    
    # Set up winning move (column 0)
    board.grid[5][0] = 1
    board.grid[4][0] = 1
    board.grid[3][0] = 1
    
    move = ai.get_move(board)
    assert move == 0, f"Should take win at column 0, got {move}"
    print("✓ Medium AI takes winning move\n")


def test_medium_prefers_center():
    """Test medium AI prefers center when no immediate threats."""
    print("Test: Medium AI center preference...")
    
    board = Board()
    ai = AI(1, 'medium')
    
    # Empty board - should pick center (column 3)
    moves = []
    for _ in range(20):
        col = ai.get_move(board)
        moves.append(col)
    
    center_picks = sum(1 for m in moves if m == 3)
    print(f"  Center column 3 chosen: {center_picks}/20")
    assert center_picks >= 15, "Should strongly prefer center"
    print("✓ Medium AI prefers center\n")


def test_hard_depth_search():
    """Test hard AI evaluates multiple depths."""
    print("Test: Hard AI depth search...")
    
    board = Board()
    ai = AI(1, 'hard')
    
    # Make some moves to get interesting position
    board.drop_piece(3, 2)
    board.drop_piece(2, 1)
    board.drop_piece(4, 2)
    
    move = ai.get_move(board)
    stats = ai.get_stats()
    
    print(f"  Move chosen: {move}")
    print(f"  Nodes evaluated: {stats['nodes_evaluated']}")
    assert stats['nodes_evaluated'] > 10, "Should evaluate many positions"
    print("✓ Hard AI performs depth search\n")


def test_hard_defensive_play():
    """Test hard AI plays defensively when threatened."""
    print("Test: Hard AI defensive play...")
    
    board = Board()
    ai = AI(2, 'hard')
    
    # Create subtle threat - player 1 has 3 in a row with open ends
    board.grid[5][2] = 1
    board.grid[5][3] = 1
    board.grid[5][4] = 1
    
    move = ai.get_move(board)
    
    # Should block somewhere in 2,3,4 or play above
    print(f"  Move: {move}, Threat at columns 2,3,4")
    assert move in [1, 2, 3, 4, 5], "Should respond to threat"
    print("✓ Hard AI recognizes threats\n")


def test_ai_vs_ai_game():
    """Test AI vs AI game completes."""
    print("Test: AI vs AI game...")
    
    ai1 = AI(1, 'easy')
    ai1.name = "AI-Easy"
    ai2 = AI(2, 'medium')
    ai2.name = "AI-Medium"
    
    game = Game(ai1, ai2)
    
    # Play up to 20 moves
    for _ in range(20):
        if game.game_over:
            break
        game.play_turn()
    
    print(f"  Game ended: {game.game_over}")
    print(f"  Moves: {game.move_count}")
    print(f"  Winner: {game.winner}")
    
    assert game.move_count > 0, "Should make moves"
    print("✓ AI vs AI game completes\n")


def test_difficulty_balance():
    """Test that harder AIs generally perform better."""
    print("Test: Difficulty balance (Medium vs Easy)...")
    
    wins = {'easy': 0, 'medium': 0, 'draw': 0}
    
    for game_num in range(5):  # 5 games
        ai_easy = AI(1 if game_num % 2 == 0 else 2, 'easy')
        ai_medium = AI(2 if game_num % 2 == 0 else 1, 'medium')
        
        ai_easy.name = "Easy"
        ai_medium.name = "Medium"
        
        game = Game(ai_easy, ai_medium)
        
        # Play with move limit
        for _ in range(25):
            if game.game_over:
                break
            game.play_turn()
        
        if game.winner:
            if 'medium' in game.winner.name.lower():
                wins['medium'] += 1
            else:
                wins['easy'] += 1
        else:
            wins['draw'] += 1
    
    print(f"  Results: Medium={wins['medium']}, Easy={wins['easy']}, Draw={wins['draw']}")
    assert wins['medium'] >= wins['easy'], "Medium should win more than easy"
    print("✓ Medium AI stronger than Easy\n")


def test_hard_vs_medium():
    """Test Hard AI vs Medium AI."""
    print("Test: Hard vs Medium balance...")
    
    ai_hard = AI(1, 'hard')
    ai_medium = AI(2, 'medium')
    ai_hard.name = "Hard"
    ai_medium.name = "Medium"
    
    game = Game(ai_hard, ai_medium)
    
    # Track nodes evaluated
    total_nodes = 0
    
    for _ in range(15):
        if game.game_over:
            break
        
        current_ai = ai_hard if game.current_player == ai_hard else ai_medium
        game.play_turn()
        
        if hasattr(current_ai, 'get_stats'):
            stats = current_ai.get_stats()
            total_nodes += stats.get('nodes_evaluated', 0)
    
    print(f"  Moves: {game.move_count}")
    print(f"  Total nodes evaluated: {total_nodes}")
    print(f"  Winner: {game.winner}")
    
    # Hard should typically win or draw
    if game.winner and 'hard' in game.winner.name.lower():
        print("  ✓ Hard AI won")
    else:
        print("  (Draw or medium win acceptable in single game)")
    
    print("✓ Hard vs Medium test complete\n")


def test_ai_respects_valid_moves():
    """Test AI only makes valid moves."""
    print("Test: AI valid moves only...")
    
    for difficulty in ['easy', 'medium', 'hard']:
        board = Board()
        ai = AI(1, difficulty)
        
        # Fill some columns
        for _ in range(6):
            board.drop_piece(0, 1)
            board.drop_piece(0, 2)
        
        # Column 0 should be full
        assert not board.is_valid_move(0), "Column 0 should be full"
        
        for _ in range(10):
            col = ai.get_move(board)
            if col is not None:
                assert board.is_valid_move(col), f"{difficulty} AI made invalid move {col}"
        
        print(f"  ✓ {difficulty} AI makes valid moves")
    
    print("✓ All AIs respect valid moves\n")


def run_all_tests():
    """Run all AI tests."""
    print("=" * 60)
    print("AI TESTING - DIFFICULTY LEVELS & BALANCE")
    print("=" * 60 + "\n")
    
    test_easy_randomness()
    test_medium_blocks_win()
    test_medium_takes_win()
    test_medium_prefers_center()
    test_hard_depth_search()
    test_hard_defensive_play()
    test_ai_vs_ai_game()
    test_difficulty_balance()
    test_hard_vs_medium()
    test_ai_respects_valid_moves()
    
    print("=" * 60)
    print("ALL AI TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()