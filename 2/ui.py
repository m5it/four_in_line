class ConnectFourUI:
    def __init__(self):
        self.symbols = {0: ".", 1: "X", 2: "O"}

    def display_board(self, board):
        print("\n  0 1 2 3 4 5 6")
        print("---------------")
        for row in board:
            display_row = "|".join([self.symbols[cell] for cell in row])
            print(f"|{display_row}|")
        print("---------------")

    def get_player_input(self):
        while True:
            try:
                user_input = input("Choose a column (0-6): ")
                col = int(user_input)
                if 0 <= col < 7:
                    return col
                else:
                    print("Invalid column. Please choose between 0 and 6.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def display_message(self, message):
        print(f"\n*** {message} ***")

    def display_game_over(self, winner, is_draw):
        if is_draw:
            self.display_message("It's a draw!")
        else:
            player_name = "Player 1 (X)" if winner == 1 else "Player 2 (O)"
            self.display_message(f"{player_name} wins!")