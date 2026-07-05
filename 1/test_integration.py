#!/usr/bin/env python3
"""Final integration tests - complete game flows."""

import sys
import os
import tempfile
import shutil

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from four_in_line.board import Board
from four_in_line.game import Game
from four_in_line.ai import AI
from four_in_line.player import Player


def test_complete_ai_game():
    """Run complete AI vs AI game to finish."""
    print("Test: Complete AI vs AI game...")
    
    ai1 = AI(1, 'medium')
    ai2 = AI(2, 'easy')
    ai1.name = "AI-Medium"
    ai2.name = "AI-Easy"
    
    game = Game(ai1, ai2)
    
    # Play until game ends (max 50 moves)
    for _ in range(50):
        if game.game_over:
            break
        game.play_turn()
    
    assert game.game_over, "Game should end"
    assert game.move_count > 0, "Should have moves"
    
    if game.winner:
        print(f"  ✓ Game ended with winner: {game.winner.name}")
    else:
        print(f"  ✓ Game ended in draw")
    
    print(f"  Total moves: {game.move_count}")
    return True


def test_all_win_conditions():
    """Verify all win types are detected."""
    print("\nTest: All win conditions...")
    
    wins = [
        ("Horizontal", lambda b: [(5, i, 1) for i in range(4)]),
        ("Vertical", lambda b: [(5-i, 0, 1) for i in range(4)]),
        ("Diagonal down-right", lambda b: [(5-i, i, 1) for i in range(4)]),
        ("Diagonal up-right", lambda b: [(2+i, i, 1) for i in range(4)]),
    ]
    
    for name, setup in wins:
        board = Board()
        positions = setup(board)
        for row, col, piece in positions:
            board.grid[row][col] = piece
        
        assert board.check_win(1), f"{name} win not detected"
        print(f"  ✓ {name} win detected")
    
    return True


def test_save_during_game():
    """Test saving during active gameplay."""
    print("\nTest: Save during active game...")
    
    test_dir = tempfile.mkdtemp()
    Game.SAVE_DIR = test_dir
    
    try:
        ai1 = AI(1, 'easy')
        ai2 = AI(2, 'easy')
        game = Game(ai1, ai2)
        
        # Play a few moves
        for _ in range(5):
            game.play_turn()
            if game.game_over:
                break
        
        # Save mid-game
        filepath = game.save("midgame.json")
        assert filepath is not None
        
        # Load and continue
        loaded = Game.load(filepath)
        assert loaded.move_count == 5
        
        # Continue playing
        for _ in range(10):
            if loaded.game_over:
                break
            loaded.play_turn()
        
        print(f"  ✓ Saved at move 5, continued to {loaded.move_count}")
        return True
        
    finally:
        shutil.rmtree(test_dir)


def test_error_handling():
    """Test graceful error handling."""
    print("\nTest: Error handling...")
    
    # Invalid column
    board = Board()
    result = board.drop_piece(-1, 1)
    assert result == -1, "Should reject negative column"
    print("  ✓ Negative column rejected")
    
    # Full column
    for _ in range(6):
        board.drop_piece(0, 1)
    result = board.drop_piece(0, 1)
    assert result == -1, "Should reject full column"
    print("  ✓ Full column rejected")
    
    # Invalid file
    try:
        Game.load("/nonexistent/path/game.json")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        print("  ✓ Missing file handled")
    
    # Corrupted JSON
    test_dir = tempfile.mkdtemp()
    bad_file = os.path.join(test_dir, "bad.json")
    with open(bad_file, 'w') as f:
        f.write("not json")
    
    try:
        Game.load(bad_file)
        assert False, "Should raise ValueError"
    except ValueError:
        print("  ✓ Corrupted file handled")
    finally:
        shutil.rmtree(test_dir)
    
    return True


def test_ai_levels_balance():
    """Quick test that AI levels show different behavior."""
    print("\nTest: AI levels differentiation...")
    
    # Easy should be random-ish
    easy_moves = []
    for _ in range(10):
        board = Board()
        ai = AI(1, 'easy')
        easy_moves.append(ai.get_move(board))
    
    # Medium should prefer center
    board = Board()
    ai = AI(1, 'medium')
    medium_move = ai.get_move(board)
    
    # Hard should evaluate more
    board = Board()
    ai = AI(1, 'hard')
    hard_move = ai.get_move(board)
    nodes = ai.get_stats()['nodes_evaluated']
    
    print(f"  Easy moves variety: {len(set(easy_moves))} unique")
    print(f"  Medium first move: {medium_move} (center preferred)")
    print(f"  Hard nodes evaluated: {nodes}")
    
    assert len(set(easy_moves)) > 1, "Easy should vary"
    assert nodes > 100, "Hard should evaluate many positions"
    print("  ✓ AI levels show different behavior")
    
    return True


def test_game_statistics():
    """Test that game statistics are accurate."""
    print("\nTest: Game statistics...")
    
    ai1 = AI(1, 'easy')
    ai2 = AI(2, 'easy')
    game = Game(ai1, ai2)
    
    # Play some moves
    for _ in range(10):
        if game.game_over:
            break
        game.play_turn()
    
    stats = {
        'moves': game.move_count,
        'history_len': len(game.move_history),
        'game_over': game.game_over,
    }
    
    assert stats['moves'] == stats['history_len'], "Move count should match history"
    assert all('player' in m for m in game.move_history), "History should have player names"
    assert all('col' in m for m in game.move_history), "History should have columns"
    
    print(f"  Moves: {stats['moves']}")
    print(f"  Game over: {stats['game_over']}")
    print("  ✓ Statistics accurate")
    
    return True


def run_all_tests():
    """Run all integration tests."""
    print("=" * 60)
    print("FINAL INTEGRATION TESTS")
    print("=" * 60)
    
    tests = [
        test_complete_ai_game,
        test_all_win_conditions,
        test_save_during_game,
        test_error_handling,
        test_ai_levels_balance,
        test_game_statistics,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n  ✗ FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)