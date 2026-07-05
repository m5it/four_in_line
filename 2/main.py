from engine import ConnectFourEngine
from ui import ConnectFourUI

def main():
    engine = ConnectFourEngine()
    ui = ConnectFourUI()
    
    print("Welcome to Connect Four!")
    
    game_over = False
    
    while not game_over:
        ui.display_board(engine.get_board())
        current_player = engine.current_player
        print(f"Player {current_player}'s turn.")
        
        col = ui.get_player_input()
        
        success = engine.drop_piece(col)
        if not success:
            print("Column is full! Try another one.")
            continue
            
        if engine.check_win():
            ui.display_board(engine.get_board())
            ui.display_game_over(engine.current_player, False)
            game_over = True
        elif engine.is_draw():
            ui.display_board(engine.get_board())
            ui.display_game_over(None, True)
            game_over = True
        else:
            engine.switch_player()

if __name__ == "__main__":
    main()