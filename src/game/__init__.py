"""
Game package initialization.
"""

# Import key classes to make them available at package level
try:
    from .player import Player
    from .engine import GameEngine
except ImportError:
    # Don't fail on import errors - let specific modules handle them
    pass