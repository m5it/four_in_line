import unittest
from engine import ConnectFourEngine

class TestConnectFour(unittest.TestCase):
    def setUp(self):
        self.engine = ConnectFourEngine()

    def test_initial_board(self):
        board = self.engine.get_board()
        self.assertEqual(len(board), 6)
        self.assertEqual(len(board[0]), 7)
        for row in board:
            for cell in row:
                self.assertEqual(cell, 0)

    def test_win_horizontal(self):
        # Manually set up a horizontal win for Player 1
        # Row 5: 1 1 1 1 0 0 0
        self.engine.board[5][0] = 1
        self.engine.board[5][1] = 1
        self.engine.board[5][2] = 1
        self.engine.board[5][3] = 1
        self.assertTrue(self.engine.check_win())

    def test_win_vertical(self):
        # Manually set up a vertical win for Player 2
        # Col 0: 2 2 2 2 0 0
        self.engine.board[5][0] = 2
        self.engine.board[4][0] = 2
        self.engine.board[3][0] = 2
        self.engine.board[2][0] = 2
        self.assertTrue(self.engine.check_win())

    def test_win_diagonal(self):
        # Manually set up a diagonal win
        self.engine.board[5][0] = 1
        self.engine.board[4][1] = 1
        self.engine.board[3][2] = 1
        self.engine.board[2][3] = 1
        self.assertTrue(self.engine.check_win())

    def test_draw(self):
        # Fill the board
        for r in range(6):
            for c in range(7):
                self.engine.board[r][c] = 1 if (r + c) % 2 == 0 else 2
        self.assertTrue(self.engine.is_draw())

    def test_drop_piece_full_column(self):
        # Fill column 0
        for r in range(6):
            self.engine.board[r][0] = 1
        # Try to drop in column 0
        success = self.engine.drop_piece(0)
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()