import sys
from ui.ascii_art import display_title
from utils.config import Config

def main():
    # Display the game title
    display_title()

    # Create a player
    from game.player import Player
    player_name = input("Enter your name: ")
    player = Player(player_name)
    
    # Create and start the game engine
    from game.engine import GameEngine
    engine = GameEngine(player)
    engine.start()

if __name__ == "__main__":
    main()