class ConnectFourEngine:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1

    def drop_piece(self, col):
        if col < 0 or col >= self.cols:
            return False
        
        # Find the lowest empty row in the selected column
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                return True
        return False

    def check_win(self):
        # Check horizontal, vertical, and diagonal wins
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 0:
                    continue
                
                player = self.board[r][c]
                # Directions: (dr, dc)
                directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
                
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        nr, nc = r + dr * i, c + dc * i
                        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[r + dr * i][c + dc * i] == player:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
        return False

    def is_draw(self):
        for c in range(self.cols):
            if self.board[0][c] == 0:
                return False
        return True

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def get_board(self):
        return self.board