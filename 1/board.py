"""Four in a Line - Board Module"""

class Board:
    """Represents a 7x6 Connect Four board."""
    
    ROWS = 6
    COLS = 7
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2
    
    def __init__(self):
        """Initialize empty board."""
        self.grid = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.winning_positions = []
    
    def display(self):
        """Render board with unicode box-drawing characters."""
        # Column headers
        print("  " + " ".join(str(i + 1) for i in range(self.COLS)))
        print(" ┌" + "─┬" * (self.COLS - 1) + "─┐")
        
        for row in range(self.ROWS):
            row_str = " │"
            for col in range(self.COLS):
                piece = self.grid[row][col]
                if piece == self.EMPTY:
                    row_str += "  │"
                elif piece == self.PLAYER1:
                    row_str += "\033[91m●\033[0m │"  # Red
                else:
                    row_str += "\033[93m●\033[0m │"  # Yellow
            print(row_str)
            if row < self.ROWS - 1:
                print(" ├" + "─┼" * (self.COLS - 1) + "─┤")
        
        print(" └" + "─┴" * (self.COLS - 1) + "─┘")
    
    def drop_piece(self, col, player):
        """Drop piece into column. Returns row or -1 if full."""
        if not self.is_valid_move(col):
            return -1
        
        # Find lowest empty row (bottom-up)
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                self.grid[row][col] = player
                return row
        return -1
    
    def is_valid_move(self, col):
        """Check if column is valid and not full."""
        if col < 0 or col >= self.COLS:
            return False
        return self.grid[0][col] == self.EMPTY
    
    def get_valid_moves(self):
        """Return list of valid columns."""
        return [col for col in range(self.COLS) if self.is_valid_move(col)]
    
    def check_win(self, player):
        """Check if player has four in a line."""
        self.winning_positions = []
        
        # Check horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.grid[row][col + i] == player for i in range(4)):
                    self.winning_positions = [(row, col + i) for i in range(4)]
                    return True
        
        # Check vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if all(self.grid[row + i][col] == player for i in range(4)):
                    self.winning_positions = [(row + i, col) for i in range(4)]
                    return True
        
        # Check diagonal (down-right)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(self.grid[row + i][col + i] == player for i in range(4)):
                    self.winning_positions = [(row + i, col + i) for i in range(4)]
                    return True
        
        # Check diagonal (up-right)
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.grid[row - i][col + i] == player for i in range(4)):
                    self.winning_positions = [(row - i, col + i) for i in range(4)]
                    return True
        
        return False
    
    def get_winning_positions(self):
        """Return coordinates of winning line."""
        return self.winning_positions
    
    def is_full(self):
        """Check if board is completely filled."""
        return all(self.grid[0][col] != self.EMPTY for col in range(self.COLS))
    
    def copy(self):
        """Create deep copy of board."""
        new_board = Board()
        new_board.grid = [row[:] for row in self.grid]
        return new_board
    
    def __str__(self):
        """String representation for debugging."""
        lines = []
        for row in self.grid:
            line = "".join(str(cell) for cell in row)
            lines.append(line)
        return "\n".join(lines)


# Test functions
def test_horizontal_win():
    """Test horizontal win detection."""
    board = Board()
    board.grid[5] = [1, 1, 1, 1, 0, 0, 0]  # Bottom row
    assert board.check_win(1) == True
    assert board.get_winning_positions() == [(5, 0), (5, 1), (5, 2), (5, 3)]
    print("✓ Horizontal win test passed")

def test_vertical_win():
    """Test vertical win detection."""
    board = Board()
    for row in range(3, 6):
        board.grid[row][2] = 2
    assert board.check_win(2) == False  # Only 3
    board.grid[2][2] = 2  # Add 4th
    assert board.check_win(2) == True
    print("✓ Vertical win test passed")

def test_diagonal_win():
    """Test diagonal win detection."""
    board = Board()
    # Down-right diagonal
    for i in range(4):
        board.grid[5 - i][i] = 1
    assert board.check_win(1) == True
    print("✓ Diagonal (down-right) win test passed")
    
    # Up-right diagonal
    board2 = Board()
    for i in range(4):
        board2.grid[2 + i][i] = 2
    assert board2.check_win(2) == True
    print("✓ Diagonal (up-right) win test passed")

def test_no_win():
    """Test no win scenario."""
    board = Board()
    assert board.check_win(1) == False
    assert board.check_win(2) == False
    print("✓ No win test passed")

def test_near_win():
    """Test near-win scenarios (3 in a row)."""
    board = Board()
    board.grid[5] = [1, 1, 1, 0, 0, 0, 0]  # 3 in a row, no win
    assert board.check_win(1) == False
    print("✓ Near-win test passed")

def run_all_tests():
    """Run all board tests."""
    print("Running Board tests...")
    test_horizontal_win()
    test_vertical_win()
    test_diagonal_win()
    test_no_win()
    test_near_win()
    print("All tests passed!")

if __name__ == "__main__":
    run_all_tests()