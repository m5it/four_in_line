"""Four in a Line - A terminal-based Connect Four game."""

__version__ = "1.0.0"
__author__ = "AI Assistant"

from .board import Board
from .game import Game
from .player import Player
from .ai import AI

__all__ = ['Board', 'Game', 'Player', 'AI']