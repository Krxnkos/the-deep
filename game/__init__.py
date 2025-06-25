"""
This module initializes the game package for The Deep adventure game.
"""

# Import necessary components for the game
from .engine import GameEngine
from .game_state import GameState
from .player import Player

# Initialize game components
game_engine = GameEngine()
game_state = GameState()
player = Player()