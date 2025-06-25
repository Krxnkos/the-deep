class Location:
    def __init__(self, id, name, description, exits=None, items=None):
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits or {}  # Dictionary of direction -> location_id
        self.items = items or []  # List of items in this location
        self.visited = False
    
    def add_exit(self, direction, location_id):
        """Add an exit to another location."""
        self.exits[direction] = location_id
    
    def remove_exit(self, direction):
        """Remove an exit."""
        if direction in self.exits:
            del self.exits[direction]
    
    def add_item(self, item):
        """Add an item to this location."""
        if item not in self.items:
            self.items.append(item)
    
    def remove_item(self, item):
        """Remove an item from this location."""
        if item in self.items:
            self.items.remove(item)

# Global dictionary to store all locations
_locations = {}

# Define locations based on the game brief
def _initialize_locations():
    """Initialize all game locations."""
    global _locations
    
    # 1. Abandoned Deep-Sea Research Station "Erebus-9"
    erebus9 = Location(
        "erebus9",
        "Abandoned Deep-Sea Research Station \"Erebus-9\"",
        """The dimly lit corridors of Erebus-9 stretch before you, water dripping from the ceiling.
        Emergency lights cast an eerie red glow across the metal walls, now covered in algae and rust.
        The silence is punctuated only by the occasional groan of metal under pressure."""
    )
    
    # 2. The Trench (Abyssal Rift)
    trench = Location(
        "trench",
        "The Trench (Abyssal Rift)",
        """A seemingly bottomless void stretches below your submersible. The depth meter 
        spins wildly as you descend. Strange bioluminescent creatures drift past your 
        viewport, some in shapes marine biologists have never documented."""
    )
    
    # 3. Ghost Reef
    ghost_reef = Location(
        "ghost_reef",
        "Ghost Reef",
        """Bleached coral stretches as far as your light can penetrate. Plastic waste and 
        industrial sludge coat what was once vibrant marine life. As you move through the reef,
        you swear you can hear faint whispers carried in the current."""
    )
    
    # 4. Derelict Fishing Trawler
    fishing_trawler = Location(
        "fishing_trawler",
        "Derelict Fishing Trawler",
        """The abandoned trawler sits at an angle, half-buried in silt. Rust has eaten through 
        much of the hull, and marine life has claimed the deck. Inside, equipment lies scattered 
        as if the crew left in a hurry. Chemical containers with hazard symbols are strewn about."""
    )
    
    # 5. The Black Bloom
    black_bloom = Location(
        "black_bloom",
        "The Black Bloom",
        """Towering stalks of inky kelp sway in the current, creating a forest of darkness. 
        The water here is noticeably warmer and has an oily quality. Sound behaves strangely, 
        seeming to come from all directions at once. Some of the kelp tendrils appear to move 
        independently of the current."""
    )
    
    # Set up exits (connections between locations)
    erebus9.add_exit("north", "trench")
    erebus9.add_exit("east", "ghost_reef")
    erebus9.add_exit("west", "fishing_trawler")
    
    trench.add_exit("south", "erebus9")
    trench.add_exit("down", "black_bloom")
    
    ghost_reef.add_exit("west", "erebus9")
    
    fishing_trawler.add_exit("east", "erebus9")
    
    black_bloom.add_exit("up", "trench")
    
    # Store locations
    _locations = {
        "erebus9": erebus9,
        "trench": trench,
        "ghost_reef": ghost_reef,
        "fishing_trawler": fishing_trawler,
        "black_bloom": black_bloom
    }

# Initialize locations when module is imported
_initialize_locations()

def get_location_by_id(location_id):
    """Get a location by its ID."""
    if location_id in _locations:
        return _locations[location_id]
    return None

def get_starting_location():
    """Get the initial starting location for the game."""
    return _locations["erebus9"]

def get_all_locations():
    """Get all locations in the game."""
    return _locations.values()