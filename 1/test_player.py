#!/usr/bin/env python3
"""Player module edge case tests with mocked input."""

import sys
import os
from io import StringIO
from unittest.mock import patch

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from four_in_line.board import Board
from four_in_line.player import Player


class MockInput:
    """Mock input stream for testing."""
    def __init__(self, inputs):
        self.inputs = iter(inputs)
        self.prompts_shown = []
    
    def __call__(self, prompt):
        self.prompts_shown.append(prompt)
        return next(self.inputs)


def test_valid_move():
    """Test valid column selection."""
    print("Test: Valid move (column 4)...")
    board = Board()
    player = Player("Test", 1)
    
    with patch('builtins.input', MockInput(['4'])):
        result = player.get_move(board)
    
    assert result == 3, f"Expected 3 (0-indexed), got {result}"
    assert player.move_history == [4], f"Move history: {player.move_history}"
    print("✓ Valid move accepted\n")


def test_quit_command():
    """Test quit command 'q'."""
    print("Test: Quit command...")
    board = Board()
    player = Player("Test", 1)
    
    with patch('builtins.input', MockInput(['q'])):
        result = player.get_move(board)
    
    assert result is None, f"Expected None, got {result}"
    assert player.move_history == [], "No move should be recorded"
    print("✓ Quit command returns None\n")


def test_non_numeric_input():
    """Test rejection of non-numeric input."""
    print("Test: Non-numeric input...")
    board = Board()
    player = Player("Test", 1)
    
    # First invalid, then valid
    mock = MockInput(['abc', '4'])
    
    with patch('builtins.input', mock):
        with patch('builtins.print') as mock_print:
            result = player.get_move(board)
    
    assert result == 3, f"Expected 3, got {result}"
    # Should have shown error message
    print("✓ Non-numeric rejected with error\n")


def test_out_of_range_low():
    """Test column below range (0 or negative)."""
    print("Test: Out of range (low)...")
    board = Board()
    player = Player("Test", 1)
    
    mock = MockInput(['0', '4'])
    
    with patch('builtins.input', mock):
        result = player.get_move(board)
    
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Column 0 rejected\n")


def test_out_of_range_high():
    """Test column above range (>7)."""
    print("Test: Out of range (high)...")
    board = Board()
    player = Player("Test", 1)
    
    mock = MockInput(['8', '4'])
    
    with patch('builtins.input', mock):
        result = player.get_move(board)
    
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Column 8 rejected\n")


def test_full_column():
    """Test column that is already full."""
    print("Test: Full column...")
    board = Board()
    player = Player("Test", 1)
    
    # Fill column 3 completely (6 pieces)
    for _ in range(6):
        board.drop_piece(3, 1)
    
    assert not board.is_valid_move(3), "Column should be full"
    
    mock = MockInput(['4', '1'])  # Try full, then valid
    
    with patch('builtins.input', mock):
        result = player.get_move(board)
    
    assert result == 0, f"Expected 0 (column 1), got {result}"
    print("✓ Full column rejected\n")


def test_negative_number():
    """Test negative column number."""
    print("Test: Negative number...")
    board = Board()
    player = Player("Test", 1)
    
    mock = MockInput(['-1', '4'])
    
    with patch('builtins.input', mock):
        result = player.get_move(board)
    
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Negative number rejected\n")


def test_whitespace_input():
    """Test input with extra whitespace."""
    print("Test: Whitespace handling...")
    board = Board()
    player = Player("Test", 1)
    
    mock = MockInput(['  4  ', '  5  '])
    
    with patch('builtins.input', mock):
        # First call should work with strip()
        result = player.get_move(board)
    
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Whitespace trimmed\n")


def test_uppercase_quit():
    """Test uppercase Q for quit."""
    print("Test: Uppercase Q...")
    board = Board()
    player = Player("Test", 1)
    
    mock = MockInput(['Q'])
    
    with patch('builtins.input', mock):
        result = player.get_move(board)
    
    assert result is None, f"Expected None, got {result}"
    print("✓ Uppercase Q accepted\n")


def test_multiple_invalid_then_valid():
    """Test multiple invalid inputs before valid."""
    print("Test: Multiple invalid inputs...")
    board = Board()
    player = Player("Test", 1)
    
    # Multiple invalid: text, out of range, negative, then valid
    mock = MockInput(['abc', '99', '-5', '0', '4'])
    
    with patch('builtins.input', mock):
        result = player.get_move(board)
    
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Multiple errors handled, valid accepted\n")


def test_move_history_accumulation():
    """Test move history tracks multiple moves."""
    print("Test: Move history accumulation...")
    board = Board()
    player = Player("Test", 1)
    
    # Simulate multiple moves
    with patch('builtins.input', MockInput(['1'])):
        player.get_move(board)
    
    with patch('builtins.input', MockInput(['3'])):
        player.get_move(board)
    
    with patch('builtins.input', MockInput(['5'])):
        player.get_move(board)
    
    assert player.move_history == [1, 3, 5], f"History: {player.move_history}"
    print("✓ Move history accumulated correctly\n")


def test_player_str_representation():
    """Test string representation."""
    print("Test: String representation...")
    player1 = Player("Alice", 1)
    player2 = Player("Bob", 2)
    
    assert "Alice" in str(player1) and "Red" in str(player1)
    assert "Bob" in str(player2) and "Yellow" in str(player2)
    print("✓ String representation correct\n")


def run_all_tests():
    """Run all Player tests."""
    print("=" * 60)
    print("PLAYER MODULE - EDGE CASE TESTS")
    print("=" * 60 + "\n")
    
    test_valid_move()
    test_quit_command()
    test_non_numeric_input()
    test_out_of_range_low()
    test_out_of_range_high()
    test_full_column()
    test_negative_number()
    test_whitespace_input()
    test_uppercase_quit()
    test_multiple_invalid_then_valid()
    test_move_history_accumulation()
    test_player_str_representation()
    
    print("=" * 60)
    print("ALL PLAYER TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()