"""Four in a Line - Player Module"""

class Player:
    """Human player interface."""
    
    def __init__(self, name, piece):
        self.name = name
        self.piece = piece
        self.move_history = []
    
    def get_move(self, board):
        """Prompt for and validate column input."""
        while True:
            try:
                user_input = input(f"{self.name}'s turn ({'Red' if self.piece == 1 else 'Yellow'}): Enter column (1-7) or 'q' to quit: ").strip().lower()
                
                if user_input == 'q':
                    return None  # Signal to quit
                
                col = int(user_input) - 1  # Convert to 0-indexed
                
                if not board.is_valid_move(col):
                    print("Invalid move: Column is full or out of range. Try again.")
                    continue
                
                self.move_history.append(col + 1)
                return col
                
            except ValueError:
                print("Invalid input: Please enter a number 1-7 or 'q' to quit.")
    
    def __str__(self):
        return f"{self.name} ({'Red' if self.piece == 1 else 'Yellow'})"