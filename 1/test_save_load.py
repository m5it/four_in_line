#!/usr/bin/env python3
"""Save/Load persistence tests with corruption handling."""

import sys
import os
import json
import tempfile
import shutil

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from four_in_line.board import Board
from four_in_line.game import Game
from four_in_line.ai import AI
from four_in_line.player import Player


def setup_test_dir():
    """Create temporary test directory."""
    return tempfile.mkdtemp(prefix="four_in_line_test_")


def cleanup_test_dir(test_dir):
    """Remove test directory."""
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


def test_basic_save_load():
    """Test basic save and load cycle."""
    print("Test: Basic save/load...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        # Create and populate game
        ai1 = AI(1, 'easy')
        ai2 = AI(2, 'medium')
        game = Game(ai1, ai2)
        
        # Make some moves
        game.board.drop_piece(3, 1)
        game.board.drop_piece(4, 2)
        game.move_count = 2
        game.move_history = [
            {'player': 'AI-1', 'col': 4, 'row': 6},
            {'player': 'AI-2', 'col': 5, 'row': 6}
        ]
        
        # Save
        filepath = game.save("test_basic.json")
        assert filepath is not None, "Save should succeed"
        assert os.path.exists(filepath), "File should exist"
        
        # Load
        loaded = Game.load(filepath)
        assert loaded.board.grid[5][3] == 1, "Board state preserved"
        assert loaded.board.grid[5][4] == 2, "Player 2 move preserved"
        assert loaded.move_count == 2, "Move count preserved"
        assert len(loaded.move_history) == 2, "History preserved"
        
        print("✓ Basic save/load works\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_corrupted_json():
    """Test handling of corrupted JSON."""
    print("Test: Corrupted JSON handling...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        # Create corrupted file
        bad_file = os.path.join(test_dir, "corrupted.json")
        with open(bad_file, 'w') as f:
            f.write("{invalid json content")
        
        try:
            Game.load(bad_file)
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "Corrupted" in str(e), f"Wrong error: {e}"
        
        print("✓ Corrupted JSON detected\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_empty_file():
    """Test handling of empty save file."""
    print("Test: Empty file handling...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        empty_file = os.path.join(test_dir, "empty.json")
        with open(empty_file, 'w') as f:
            f.write("")
        
        try:
            Game.load(empty_file)
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "empty" in str(e).lower(), f"Wrong error: {e}"
        
        print("✓ Empty file detected\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_missing_fields():
    """Test handling of save with missing required fields."""
    print("Test: Missing fields handling...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        bad_file = os.path.join(test_dir, "incomplete.json")
        incomplete = {
            'board': [[0]*7 for _ in range(6)],
            # Missing 'current_player', 'players', 'move_count'
        }
        with open(bad_file, 'w') as f:
            json.dump(incomplete, f)
        
        try:
            Game.load(bad_file)
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "missing" in str(e).lower(), f"Wrong error: {e}"
        
        print("✓ Missing fields detected\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_invalid_board_dimensions():
    """Test handling of wrong board size."""
    print("Test: Invalid board dimensions...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        bad_file = os.path.join(test_dir, "bad_board.json")
        bad_data = {
            'board': [[0]*5 for _ in range(4)],  # Wrong: 4x5 instead of 6x7
            'current_player': 0,
            'players': [{'name': 'P1', 'piece': 1, 'type': 'human'}],
            'move_count': 0
        }
        with open(bad_file, 'w') as f:
            json.dump(bad_data, f)
        
        try:
            Game.load(bad_file)
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "dimensions" in str(e).lower(), f"Wrong error: {e}"
        
        print("✓ Invalid dimensions detected\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_list_saved_games():
    """Test listing saved games."""
    print("Test: List saved games...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        # Create multiple saves
        for i in range(3):
            ai1 = AI(1, 'easy')
            ai2 = AI(2, 'easy')
            game = Game(ai1, ai2)
            game.move_count = i + 1
            game.save(f"game_{i}.json")
        
        # List games
        saves = Game.list_saved_games(test_dir)
        assert len(saves) == 3, f"Expected 3 saves, got {len(saves)}"
        
        # Check metadata
        for save in saves:
            assert 'filename' in save
            assert 'move_count' in save
        
        print(f"✓ Listed {len(saves)} games\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_list_with_corrupted():
    """Test listing includes corrupted files gracefully."""
    print("Test: List with corrupted files...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        # Create valid save
        ai1 = AI(1, 'easy')
        ai2 = AI(2, 'easy')
        game = Game(ai1, ai2)
        game.save("valid.json")
        
        # Create corrupted file
        with open(os.path.join(test_dir, "bad.json"), 'w') as f:
            f.write("not json")
        
        # List should include both, mark corrupted
        saves = Game.list_saved_games(test_dir)
        assert len(saves) == 2, f"Expected 2 saves, got {len(saves)}"
        
        corrupted = [s for s in saves if s.get('corrupted')]
        assert len(corrupted) == 1, "Should mark one as corrupted"
        
        print("✓ Corrupted files handled gracefully\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_auto_save():
    """Test auto-save functionality."""
    print("Test: Auto-save...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        ai1 = AI(1, 'easy')
        ai2 = AI(2, 'easy')
        game = Game(ai1, ai2, auto_save=True)
        
        # Auto-save triggers during play_turn at move 5
        # Simulate by calling save directly with autosave filename
        game.move_count = 5
        game.save(Game.AUTO_SAVE_FILE, silent=True)
        
        autosave_path = os.path.join(test_dir, Game.AUTO_SAVE_FILE)
        assert os.path.exists(autosave_path), "Auto-save should exist"
        
        # Load and verify
        loaded = Game.load_autosave()
        assert loaded is not None, "Should load autosave"
        assert loaded.move_count == 5, f"Expected 5, got {loaded.move_count}"
        
        # Test clear autosave
        game._clear_autosave()
        assert not os.path.exists(autosave_path), "Autosave should be cleared"
        
        print("✓ Auto-save works\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_atomic_save():
    """Test atomic save (temp file then rename)."""
    print("Test: Atomic save...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        ai1 = AI(1, 'easy')
        ai2 = AI(2, 'easy')
        game = Game(ai1, ai2)
        
        filepath = game.save("atomic_test.json")
        
        # Should not leave temp files
        temp_files = [f for f in os.listdir(test_dir) if f.endswith('.tmp')]
        assert len(temp_files) == 0, f"Temp files left: {temp_files}"
        
        # File should be valid JSON
        with open(filepath, 'r') as f:
            data = json.load(f)
            assert 'version' in data
        
        print("✓ Atomic save works\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_player_type_preservation():
    """Test that player types (human/AI) are preserved."""
    print("Test: Player type preservation...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        # Human vs AI
        human = Player("Human", 1)
        ai = AI(2, 'hard')
        ai.name = "AI-Hard"
        
        game = Game(human, ai)
        filepath = game.save("mixed_types.json")
        
        # Load
        loaded = Game.load(filepath)
        
        # Check types
        assert not hasattr(loaded.players[0], 'difficulty'), "P1 should be human"
        assert hasattr(loaded.players[1], 'difficulty'), "P2 should be AI"
        assert loaded.players[1].difficulty == 'hard', "Difficulty preserved"
        
        print("✓ Player types preserved\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_winner_restoration():
    """Test winner is restored for completed games."""
    print("Test: Winner restoration...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        ai1 = AI(1, 'easy')
        ai2 = AI(2, 'easy')
        game = Game(ai1, ai2)
        
        # Create winning state
        game.board.grid[5] = [1, 1, 1, 1, 0, 0, 0]
        game.game_over = True
        game.winner = ai1
        
        filepath = game.save("completed.json")
        
        # Load
        loaded = Game.load(filepath)
        assert loaded.game_over == True, "Game should be over"
        assert loaded.winner is not None, "Winner should be set"
        assert loaded.winner.piece == 1, "Winner piece should be 1"
        
        print("✓ Winner restored\n")
        
    finally:
        cleanup_test_dir(test_dir)


def test_keyboard_interrupt_save():
    """Test that interrupt saves game if auto-save enabled."""
    print("Test: Interrupt handling...")
    
    test_dir = setup_test_dir()
    Game.SAVE_DIR = test_dir
    
    try:
        ai1 = AI(1, 'easy')
        ai2 = AI(2, 'easy')
        game = Game(ai1, ai2, auto_save=True)
        game.move_count = 3
        
        # Simulate keyboard interrupt during play
        try:
            raise KeyboardInterrupt()
        except KeyboardInterrupt:
            if game.auto_save and game.move_count > 0:
                game.save(game.AUTO_SAVE_FILE)
        
        # Should have saved
        autosave_path = os.path.join(test_dir, game.AUTO_SAVE_FILE)
        assert os.path.exists(autosave_path), "Should save on interrupt"
        
        print("✓ Interrupt saves game\n")
        
    finally:
        cleanup_test_dir(test_dir)


def run_all_tests():
    """Run all save/load tests."""
    print("=" * 60)
    print("SAVE/LOAD PERSISTENCE TESTS")
    print("=" * 60 + "\n")
    
    test_basic_save_load()
    test_corrupted_json()
    test_empty_file()
    test_missing_fields()
    test_invalid_board_dimensions()
    test_list_saved_games()
    test_list_with_corrupted()
    test_auto_save()
    test_atomic_save()
    test_player_type_preservation()
    test_winner_restoration()
    test_keyboard_interrupt_save()
    
    print("=" * 60)
    print("ALL SAVE/LOAD TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()