"""Four in a Line - Game Module"""

import json
import os
import sys
from datetime import datetime

class Game:
    """Main game controller."""
    
    SAVE_DIR = "saves"
    AUTO_SAVE_FILE = "autosave.json"
    
    def __init__(self, player1, player2, auto_save=False):
        from .board import Board
        self.board = Board()
        self.players = [player1, player2]
        self.current_player_idx = 0
        self.game_over = False
        self.winner = None
        self.move_count = 0
        self.move_history = []
        self.auto_save = auto_save
        self._last_save = None
    
    @property
    def current_player(self):
        return self.players[self.current_player_idx]
    
    def switch_player(self):
        """Toggle between players."""
        self.current_player_idx = 1 - self.current_player_idx
    
    def play_turn(self):
        """Execute one turn."""
        self.board.display()
        print(f"\n{self.current_player}'s turn")
        
        col = self.current_player.get_move(self.board)
        
        if col is None:  # Quit signal
            if self.auto_save and self.move_count > 0:
                print("\nAuto-saving game...")
                self.save(self.AUTO_SAVE_FILE)
            return False
        
        row = self.board.drop_piece(col, self.current_player.piece)
        if row == -1:
            print("Error: Invalid move")
            return True
        
        self.move_count += 1
        self.move_history.append({
            'player': self.current_player.name,
            'piece': self.current_player.piece,
            'col': col + 1,
            'row': row + 1,
            'timestamp': datetime.now().isoformat()
        })
        
        # Auto-save every 5 moves if enabled
        if self.auto_save and self.move_count % 5 == 0:
            self.save(self.AUTO_SAVE_FILE, silent=True)
        
        # Check win
        if self.board.check_win(self.current_player.piece):
            self.board.display()
            print(f"\n🎉 {self.current_player} WINS! 🎉")
            self._highlight_win()
            self.game_over = True
            self.winner = self.current_player
            if self.auto_save:
                self._clear_autosave()
            return True
        
        # Check draw
        if self.board.is_full():
            self.board.display()
            print("\n🤝 It's a DRAW! 🤝")
            self.game_over = True
            if self.auto_save:
                self._clear_autosave()
            return True
        
        self.switch_player()
        return True
    
    def _highlight_win(self):
        """Show winning positions."""
        positions = self.board.get_winning_positions()
        print(f"Winning line: ", end="")
        for row, col in positions:
            print(f"({col + 1},{row + 1}) ", end="")
        print()
    
    def play(self):
        """Main game loop."""
        print("\n" + "=" * 40)
        print("    FOUR IN A LINE")
        print("=" * 40)
        
        try:
            while not self.game_over:
                if not self.play_turn():
                    print("Game abandoned.")
                    return
        except KeyboardInterrupt:
            print("\n\nGame interrupted!")
            if self.auto_save and self.move_count > 0:
                print("Auto-saving...")
                self.save(self.AUTO_SAVE_FILE)
            raise
        
        self._show_stats()
    
    def _show_stats(self):
        """Display game statistics."""
        print(f"\nTotal moves: {self.move_count}")
        print(f"Game duration: {len(self.move_history)} turns")
    
    def save(self, filename=None, silent=False):
        """Save game state to JSON."""
        if not os.path.exists(self.SAVE_DIR):
            try:
                os.makedirs(self.SAVE_DIR)
            except OSError as e:
                print(f"Error creating save directory: {e}")
                return None
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"save_{timestamp}.json"
        
        filepath = os.path.join(self.SAVE_DIR, filename)
        
        # Build state with version for compatibility
        state = {
            'version': '1.0',
            'saved_at': datetime.now().isoformat(),
            'board': self.board.grid,
            'current_player': self.current_player_idx,
            'move_count': self.move_count,
            'move_history': self.move_history,
            'game_over': self.game_over,
            'winner': self.winner.name if self.winner else None,
            'winner_piece': self.winner.piece if self.winner else None,
            'players': [
                {
                    'name': p.name, 
                    'piece': p.piece, 
                    'type': 'human' if not hasattr(p, 'difficulty') else 'ai',
                    'difficulty': getattr(p, 'difficulty', None)
                }
                for p in self.players
            ]
        }
        
        try:
            # Write to temp file first, then rename for atomicity
            temp_path = filepath + '.tmp'
            with open(temp_path, 'w') as f:
                json.dump(state, f, indent=2)
            
            # Replace old file atomically
            if os.path.exists(filepath):
                os.replace(temp_path, filepath)
            else:
                os.rename(temp_path, filepath)
            
            self._last_save = filepath
            
            if not silent:
                print(f"Game saved to {filepath}")
            return filepath
            
        except (IOError, OSError) as e:
            print(f"Error saving game: {e}")
            # Cleanup temp file if exists
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            return None
    
    def _clear_autosave(self):
        """Remove autosave file after game ends."""
        autosave_path = os.path.join(self.SAVE_DIR, self.AUTO_SAVE_FILE)
        if os.path.exists(autosave_path):
            try:
                os.remove(autosave_path)
            except OSError:
                pass
    
    @classmethod
    def load(cls, filepath):
        """Load game from JSON with error handling."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                if not content.strip():
                    raise ValueError("Save file is empty")
                state = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Corrupted save file: {e}")
        except IOError as e:
            raise IOError(f"Cannot read save file: {e}")
        
        # Validate required fields
        required = ['board', 'current_player', 'players', 'move_count']
        missing = [f for f in required if f not in state]
        if missing:
            raise ValueError(f"Save file missing fields: {', '.join(missing)}")
        
        # Validate board dimensions
        if len(state['board']) != 6 or any(len(row) != 7 for row in state['board']):
            raise ValueError("Invalid board dimensions in save file")
        
        # Recreate players
        from .player import Player
        from .ai import AI
        
        players = []
        for i, p in enumerate(state['players']):
            if not isinstance(p, dict) or 'name' not in p or 'piece' not in p:
                raise ValueError(f"Invalid player data at index {i}")
            
            if p.get('type') == 'ai':
                ai = AI(p['piece'], p.get('difficulty', 'medium'))
                ai.name = p['name']
                players.append(ai)
            else:
                players.append(Player(p['name'], p['piece']))
        
        # Create game instance
        game = cls(players[0], players[1])
        
        # Restore state
        game.board.grid = [row[:] for row in state['board']]  # Deep copy
        game.current_player_idx = state['current_player']
        game.move_count = state['move_count']
        game.move_history = state.get('move_history', [])
        game.game_over = state.get('game_over', False)
        
        # Restore winner if game was over
        winner_name = state.get('winner')
        winner_piece = state.get('winner_piece')
        if winner_name and winner_piece:
            for p in game.players:
                if p.piece == winner_piece:
                    game.winner = p
                    break
        
        return game
    
    @classmethod
    def list_saved_games(cls, directory=None):
        """List all saved games with metadata."""
        if directory is None:
            directory = cls.SAVE_DIR
        
        if not os.path.exists(directory):
            return []
        
        saves = []
        for filename in os.listdir(directory):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as f:
                    state = json.load(f)
                
                # Extract metadata
                meta = {
                    'filename': filename,
                    'filepath': filepath,
                    'move_count': state.get('move_count', 0),
                    'game_over': state.get('game_over', False),
                    'winner': state.get('winner'),
                    'saved_at': state.get('saved_at', 'unknown'),
                    'players': [p.get('name', 'Unknown') for p in state.get('players', [])]
                }
                saves.append(meta)
                
            except (json.JSONDecodeError, IOError):
                # Skip corrupted files
                saves.append({
                    'filename': filename,
                    'filepath': filepath,
                    'corrupted': True
                })
        
        # Sort by save time, newest first
        saves.sort(key=lambda x: x.get('saved_at', ''), reverse=True)
        return saves
    
    @classmethod
    def has_autosave(cls):
        """Check if autosave exists."""
        autosave_path = os.path.join(cls.SAVE_DIR, cls.AUTO_SAVE_FILE)
        return os.path.exists(autosave_path)
    
    @classmethod
    def load_autosave(cls):
        """Load autosave if exists."""
        autosave_path = os.path.join(cls.SAVE_DIR, cls.AUTO_SAVE_FILE)
        if os.path.exists(autosave_path):
            return cls.load(autosave_path)
        return None