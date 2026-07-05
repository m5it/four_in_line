"""Four in a Line - AI Module"""

import random
from functools import lru_cache

class AI:
    """AI opponent with multiple difficulty levels."""
    
    def __init__(self, piece, difficulty='medium'):
        self.piece = piece
        self.opponent = 3 - piece  # 1 if 2, 2 if 1
        self.difficulty = difficulty
        self.name = f"AI ({difficulty})"
        self.move_history = []
        self.nodes_evaluated = 0  # For debugging/search metrics
    
    def get_move(self, board):
        """Select move based on difficulty."""
        self.nodes_evaluated = 0
        
        if self.difficulty == 'easy':
            return self._easy_move(board)
        elif self.difficulty == 'medium':
            return self._medium_move(board)
        else:  # hard
            return self._hard_move(board)
    
    def _easy_move(self, board):
        """Random valid move."""
        valid = board.get_valid_moves()
        return random.choice(valid) if valid else None
    
    def _medium_move(self, board):
        """Block wins, take winning moves, prefer center."""
        valid = board.get_valid_moves()
        if not valid:
            return None
        
        # Check for winning move
        for col in valid:
            test_board = board.copy()
            test_board.drop_piece(col, self.piece)
            if test_board.check_win(self.piece):
                return col
        
        # Block opponent win
        for col in valid:
            test_board = board.copy()
            test_board.drop_piece(col, self.opponent)
            if test_board.check_win(self.opponent):
                return col
        
        # Prefer center columns
        center_prefs = [3, 2, 4, 1, 5, 0, 6]
        for col in center_prefs:
            if col in valid:
                return col
        
        return random.choice(valid)
    
    def _hard_move(self, board):
        """Minimax with alpha-beta pruning, depth 4."""
        valid = board.get_valid_moves()
        if not valid:
            return None
        
        # Immediate win/loss detection
        for col in valid:
            test = board.copy()
            test.drop_piece(col, self.piece)
            if test.check_win(self.piece):
                return col
        
        for col in valid:
            test = board.copy()
            test.drop_piece(col, self.opponent)
            if test.check_win(self.opponent):
                return col
        
        # Minimax with alpha-beta
        best_score = float('-inf')
        best_col = valid[0]
        alpha = float('-inf')
        beta = float('inf')
        
        # Search depth 4
        depth = 4
        
        # Order moves by center preference for better pruning
        ordered_moves = sorted(valid, key=lambda c: -abs(3 - c))
        
        for col in ordered_moves:
            test_board = board.copy()
            test_board.drop_piece(col, self.piece)
            score = self._minimax(test_board, depth - 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_col = col
            
            alpha = max(alpha, best_score)
        
        return best_col
    
    def _minimax(self, board, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning."""
        self.nodes_evaluated += 1
        
        # Terminal states
        if board.check_win(self.piece):
            return 100000 + depth  # Prefer faster wins
        if board.check_win(self.opponent):
            return -100000 - depth  # Delay losses
        
        if depth == 0 or board.is_full():
            return self._evaluate_board(board)
        
        valid = board.get_valid_moves()
        
        if is_maximizing:
            max_eval = float('-inf')
            for col in valid:
                test = board.copy()
                test.drop_piece(col, self.piece)
                eval = self._minimax(test, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = float('inf')
            for col in valid:
                test = board.copy()
                test.drop_piece(col, self.opponent)
                eval = self._minimax(test, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def _evaluate_board(self, board):
        """Comprehensive position evaluation."""
        score = 0
        
        # Center control (most valuable)
        center_col = 3
        for row in range(board.ROWS):
            if board.grid[row][center_col] == self.piece:
                score += 6
            elif board.grid[row][center_col] == self.opponent:
                score -= 6
        
        # Adjacent to center
        for row in range(board.ROWS):
            for col in [2, 4]:
                if board.grid[row][col] == self.piece:
                    score += 3
                elif board.grid[row][col] == self.opponent:
                    score -= 3
        
        # Evaluate all windows of 4
        score += self._evaluate_windows(board, self.piece)
        score -= self._evaluate_windows(board, self.opponent) * 1.1  # Slight defensive bias
        
        return score
    
    def _evaluate_windows(self, board, player):
        """Score all possible 4-windows."""
        score = 0
        
        # Horizontal
        for row in range(board.ROWS):
            for col in range(board.COLS - 3):
                window = [board.grid[row][col + i] for i in range(4)]
                score += self._score_window(window, player)
        
        # Vertical
        for row in range(board.ROWS - 3):
            for col in range(board.COLS):
                window = [board.grid[row + i][col] for i in range(4)]
                score += self._score_window(window, player)
        
        # Diagonal down-right
        for row in range(board.ROWS - 3):
            for col in range(board.COLS - 3):
                window = [board.grid[row + i][col + i] for i in range(4)]
                score += self._score_window(window, player)
        
        # Diagonal up-right
        for row in range(3, board.ROWS):
            for col in range(board.COLS - 3):
                window = [board.grid[row - i][col + i] for i in range(4)]
                score += self._score_window(window, player)
        
        return score
    
    def _score_window(self, window, player):
        """Score a single 4-cell window."""
        opponent = 3 - player
        
        if window.count(opponent) > 0:
            return 0  # Blocked window
        
        piece_count = window.count(player)
        
        if piece_count == 4:
            return 10000  # Win
        elif piece_count == 3:
            return 100   # Strong threat
        elif piece_count == 2:
            return 10    # Potential
        elif piece_count == 1:
            return 1     # Weak potential
        
        return 0
    
    def _count_threats(self, board, player):
        """Count 3-in-a-row threats (legacy)."""
        threats = 0
        
        # Horizontal threats
        for row in range(board.ROWS):
            for col in range(board.COLS - 3):
                window = [board.grid[row][col + i] for i in range(4)]
                if window.count(player) == 3 and window.count(0) == 1:
                    threats += 1
        
        # Vertical threats
        for row in range(board.ROWS - 3):
            for col in range(board.COLS):
                window = [board.grid[row + i][col] for i in range(4)]
                if window.count(player) == 3 and window.count(0) == 1:
                    threats += 1
        
        return threats
    
    def __str__(self):
        return self.name
    
    def get_stats(self):
        """Return search statistics."""
        return {
            'nodes_evaluated': self.nodes_evaluated,
            'difficulty': self.difficulty
        }