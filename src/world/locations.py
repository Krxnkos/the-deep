"""
Locations for The Deep game.
Defines the locations, their connections, and their contents.
"""

class Location:
    def __init__(self, id, name, description, exits=None, items=None):
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits or {}  # Dictionary of direction -> location_id
        self.items = items or []  # List of items in this location
        self.visited = False      # Track if player has been here
        
    def add_exit(self, direction, location_id):
        """Add an exit from this location."""
        self.exits[direction] = location_id
        
    def remove_exit(self, direction):
        """Remove an exit from this location."""
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

def initialize_locations():
    """Create and return a dictionary of all game locations."""
    from world.items import get_item_by_id
    
    # Create the locations dictionary
    locations = {}
    
    # Research Vessel - Starting Area
    locations["ship_deck"] = Location(
        "ship_deck",
        "Research Vessel Deck",
        "The main deck of your research vessel. Equipment is neatly organized, and the control panels hum with activity. The ocean stretches in all directions, remarkably calm today.",
        exits={"down": "observation_deck"},
        items=[get_item_by_id("binoculars")]
    )
    
    locations["observation_deck"] = Location(
        "observation_deck",
        "Observation Deck",
        "A specialized deck with reinforced glass panels allowing underwater viewing. Scientific equipment lines the walls, ready to analyze samples and data from your expedition.",
        exits={"up": "ship_deck", "down": "diving_prep"},
        items=[get_item_by_id("sample_vial")]
    )
    
    locations["diving_prep"] = Location(
        "diving_prep",
        "Diving Preparation Room",
        "A small chamber where diving gear is stored and prepared. The advanced dive suits hang on wall hooks, designed to withstand extreme depths and pressures.",
        exits={"up": "observation_deck", "down": "coral_reef"},
        items=[get_item_by_id("oxygen_tank"), get_item_by_id("small_medkit")]
    )
    
    # Shallow Waters
    locations["coral_reef"] = Location(
        "coral_reef",
        "Dying Coral Reef",
        "Once vibrant and full of life, this coral reef is now pale and bleached. Some coral structures show signs of decay, while others have completely died. Few fish swim among the skeletal remains.",
        exits={"up": "diving_prep", "down": "kelp_forest"},
        items=[get_item_by_id("water_sample"), get_item_by_id("healing_gel")]
    )
    
    locations["shallow_cave"] = Location(
        "shallow_cave",
        "Shallow Marine Cave",
        "A dimly lit underwater cave near the reef. Strange bioluminescent algae provide ghostly blue illumination. Garbage from the surface has accumulated here, carried by currents.",
        exits={"east": "coral_reef", "west": "fishing_trawler"},
        items=[get_item_by_id("plastic_sample")]
    )
    
    # Mid Waters
    locations["kelp_forest"] = Location(
        "kelp_forest",
        "Kelp Forest",
        "Towering strands of kelp sway in the underwater currents. The thick vegetation creates a maze-like environment, with beams of light filtering through from above.",
        exits={"up": "coral_reef", "down": "underwater_cliff", "west": "shallow_cave"},
        items=[]
    )
    
    locations["fishing_trawler"] = Location(
        "fishing_trawler",
        "Abandoned Fishing Trawler",
        "The rusting hulk of an industrial trawler rests on its side. Fishing nets are still draped over the sides, trapping marine life. The vessel seems to have been abandoned hastily.",
        exits={"east": "shallow_cave", "down": "trench"},
        items=[get_item_by_id("chemical_sample"), get_item_by_id("harpoon_gun")]
    )
    
    # Deep Waters
    locations["underwater_cliff"] = Location(
        "underwater_cliff",
        "Underwater Cliff Edge",
        "A dramatic drop-off where the continental shelf ends. Looking down, you can see only darkness. Strange deep-water creatures occasionally pass by, some exhibiting unusual mutations.",
        exits={"up": "kelp_forest", "down": "abyssal_plain"},
        items=[get_item_by_id("stim_pack")]
    )
    
    locations["abyssal_plain"] = Location(
        "abyssal_plain",
        "Abyssal Plain",
        "A vast, flat expanse of sea floor stretched out before you. The water pressure here is immense, and the cold is bone-chilling. Strange bioluminescent creatures provide the only natural light.",
        exits={"up": "underwater_cliff", "east": "hydrothermal_vent", "west": "trench"},
        items=[get_item_by_id("strange_artifact")]
    )
    
    # Deepest Zones
    locations["trench"] = Location(
        "trench",
        "Ocean Trench",
        "A narrow, frighteningly deep crevice in the ocean floor. Your lights barely penetrate the darkness. The walls are lined with bizarre, never-before-documented life forms.",
        exits={"east": "abyssal_plain", "up": "fishing_trawler", "down": "trench_bottom"},
        items=[]
    )
    
    locations["hydrothermal_vent"] = Location(
        "hydrothermal_vent",
        "Hydrothermal Vent Field",
        "Superheated water spews from cracks in the ocean floor, creating a surreal landscape. Despite the extreme conditions, specialized life forms thrive here, adapted to the toxic minerals.",
        exits={"west": "abyssal_plain", "south": "erebus9"},
        items=[get_item_by_id("thermal_sample"), get_item_by_id("sonic_disruptor")]
    )
    
    locations["erebus9"] = Location(
        "erebus9",
        "Erebus-9 Research Station",
        "The abandoned deep-sea research station looms before you, its metal structure encrusted with marine growth. Emergency lights still flicker, casting eerie shadows. Equipment lies scattered as if the evacuation was sudden.",
        exits={"north": "hydrothermal_vent", "east": "ghost_reef", "west": "trench_bottom"},
        items=[get_item_by_id("research_log"), get_item_by_id("large_medkit")]
    )
    
    locations["ghost_reef"] = Location(
        "ghost_reef",
        "Ghost Reef",
        "A surreal landscape of fossilized coral formations, bleached bone-white. No living coral exists here anymore. The water has a strange, oily quality and carries an unnatural luminescence.",
        exits={"west": "erebus9", "south": "black_bloom"},
        items=[get_item_by_id("mutated_coral")]
    )
    
    locations["trench_bottom"] = Location(
        "trench_bottom",
        "Trench Bottom",
        "The crushing depths of the trench bottom. Strange rock formations and alien-looking creatures inhabit this rarely-seen environment. A faint pulsing light emanates from the east.",
        exits={"up": "trench", "east": "erebus9"},
        items=[get_item_by_id("pressure_sample"), get_item_by_id("plasma_cutter")]
    )
    
    # Final Area
    locations["black_bloom"] = Location(
        "black_bloom",
        "The Black Bloom",
        "A massive, pulsating growth of black algae-like material covers the sea floor. At its center, something that appears almost like a face or mouth shifts and moves. The water here feels wrong - thicker, colder, somehow aware.",
        exits={"north": "ghost_reef"},
        items=[get_item_by_id("elson_final_notes")]
    )
    
    return locations

def get_starting_location():
    """Return the starting location for the game."""
    locations = initialize_locations()
    return locations["ship_deck"]