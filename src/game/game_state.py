"""
Game state module for The Deep game.
Manages the game world, locations, and state.
"""

from world.locations import initialize_locations

class GameState:
    """Manages the game world state, including locations and game progression."""
    
    def __init__(self):
        """Initialize the game state with all locations."""
        self.locations = initialize_locations()
        
        # Set the starting location
        self.starting_location_id = "ship_deck"
        self.current_location = self.get_location(self.starting_location_id)
        
        # Track game progression
        self.visited_locations = set()
        self.game_flags = {}
        
    def get_location(self, location_id):
        """Get a location by its ID."""
        if location_id in self.locations:
            return self.locations[location_id]
        else:
            # Return a default location if the ID is not found
            return None
            
    def set_flag(self, flag_name, value=True):
        """Set a game flag to track progression or events."""
        self.game_flags[flag_name] = value
        
    def check_flag(self, flag_name):
        """Check if a game flag is set."""
        return self.game_flags.get(flag_name, False)
        
    def mark_location_visited(self, location_id):
        """Mark a location as visited."""
        self.visited_locations.add(location_id)
        
    def is_location_visited(self, location_id):
        """Check if a location has been visited."""
        return location_id in self.visited_locations