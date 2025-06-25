class GameEngine:
    def __init__(self, player=None):
        from game.player import Player
        self.player = player if player else Player("Explorer")
        self.game_running = False
        self.current_location = None
        # Other initialization code...
    
    def start(self):
        """Start the game engine and begin the game."""
        self.game_running = True
        self.display_intro()
        
        # Main game loop
        while self.game_running:
            self.process_current_location()
            self.handle_player_input()
            
            # Check game over conditions
            if self.player.health <= 0:
                self.game_over("You have succumbed to the depths...")
                break
    
    def display_intro(self):
        """Display the game introduction sequence."""
        from ui.ascii_art import display_title
        from ui.text_effects import typewriter_effect
        
        display_title()
        intro_text = """
        WELCOME TO THE DEEP
        
        Beneath the surface lies more than darkness.
        
        You are about to embark on a perilous journey to uncover 
        the mysteries of the abandoned deep-sea research station Erebus-9.
        
        Steel your nerves. Not everything you see or hear can be trusted.
        """
        typewriter_effect(intro_text)
        input("\nPress ENTER to begin your descent...")
    
    def process_current_location(self):
        """Process the current location and display relevant information."""
        if not self.current_location:
            # Set initial location if none exists
            from world.locations import get_starting_location
            self.current_location = get_starting_location()
            
        # Display location information
        print(f"\n=== {self.current_location.name} ===")
        print(self.current_location.description)
        
        # Display available exits
        if self.current_location.exits:
            print("\nPossible directions:")
            for direction, location_id in self.current_location.exits.items():
                print(f"- {direction}")
    
    def handle_player_input(self):
        """Process player input for the current game state."""
        action = input("\nWhat would you like to do? > ").lower().strip()
        
        # Handle movement
        if action in ["north", "south", "east", "west", "up", "down"]:
            self.move_player(action)
        # Handle inventory
        elif action == "inventory" or action == "i":
            print(self.player.show_inventory())
        # Handle examination
        elif action.startswith("examine ") or action.startswith("look at "):
            item = action.replace("examine ", "").replace("look at ", "")
            self.examine_item(item)
        # Handle help
        elif action == "help":
            self.show_help()
        # Handle quit
        elif action == "quit":
            if input("Are you sure you want to quit? (y/n) ").lower() == "y":
                self.game_running = False
        else:
            print("I don't understand that command.")
    
    def move_player(self, direction):
        """Move the player in the specified direction."""
        if direction in self.current_location.exits:
            from world.locations import get_location_by_id
            next_location_id = self.current_location.exits[direction]
            self.current_location = get_location_by_id(next_location_id)
            self.player.set_location(self.current_location.id)
        else:
            print(f"You can't go {direction} from here.")
    
    def examine_item(self, item_name):
        """Examine an item in the environment or inventory."""
        # Check if item is in the current location
        for item in self.current_location.items:
            if item.name.lower() == item_name:
                print(item.description)
                return
                
        # Check if item is in inventory
        for item in self.player.inventory:
            if item.name.lower() == item_name:
                print(item.description)
                return
                
        print(f"You don't see a {item_name} here.")
    
    def show_help(self):
        """Display help information for the player."""
        help_text = """
        AVAILABLE COMMANDS:
        - north, south, east, west, up, down: Move in a direction
        - inventory (or i): Check your inventory
        - examine [item]: Look closely at an item
        - take [item]: Pick up an item
        - use [item]: Use an item from your inventory
        - help: Display this help message
        - quit: Exit the game
        """
        print(help_text)
    
    def game_over(self, message):
        """End the game with the specified message."""
        print("\n" + "="*50)
        print("GAME OVER")
        print(message)
        print("="*50)
        self.game_running = False