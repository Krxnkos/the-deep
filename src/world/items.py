class Item:
    def __init__(self, id, name, description, usable=True):
        self.id = id
        self.name = name
        self.description = description
        self.usable = usable
    
    def use(self, player, location):
        """Default use method - override in subclasses"""
        return f"You use the {self.name}, but nothing special happens."

class Weapon(Item):
    def __init__(self, id, name, description, damage, durability=100):
        super().__init__(id, name, description, usable=True)
        self.damage = damage
        self.max_durability = durability
        self.durability = durability
    
    def use(self, player, location=None):
        if self.durability <= 0:
            return f"The {self.name} is broken and cannot be used."
        
        return f"You ready the {self.name}."
    
    def attack(self, target):
        if self.durability <= 0:
            return 0, f"The {self.name} is broken and cannot be used."
        
        damage_dealt = self.damage
        self.durability -= 5  # Weapon degradation on use
        
        if self.durability <= 0:
            result = f"You attack with the {self.name} dealing {damage_dealt} damage. The {self.name} breaks from the strain!"
        else:
            result = f"You attack with the {self.name} dealing {damage_dealt} damage. Durability: {self.durability}/{self.max_durability}"
        
        return damage_dealt, result

# Define game items from the brief
def initialize_items():
    items = {
        "abyssal_scanner": Item(
            "abyssal_scanner",
            "Abyssal Scanner",
            """A handheld device that pulses with soft blue light. It can detect movement and heat signatures 
            through walls, but sometimes it picks up things that don't seem to be there."""
        ),
        
        "waterproof_journal": Item(
            "waterproof_journal",
            "Waterproof Journal",
            """A sturdy journal with synthetic pages that repel water. Previous researchers have 
            filled it with notes, sketches, and observations about the deep sea ecosystem."""
        ),
        
        "coral_sample": Item(
            "coral_sample",
            "Corrupted Coral Sample",
            """A fist-sized piece of coral that emits an unnatural glow. The closer you get to 
            paranormal events, the brighter it pulses. Its shape seems to be slowly changing."""
        ),
        
        "divers_talisman": Item(
            "divers_talisman",
            "Diver's Talisman",
            """A strange amulet made from polished bone and sea glass. Local legends say it 
            protects from "what sleeps in the tide." It feels unusually warm to the touch."""
        ),
        
        "flare_gun": Weapon(
            "flare_gun",
            "Emergency Flare Gun",
            """A standard emergency flare gun with limited ammunition. It provides light 
            in dark places but also attracts attention - both wanted and unwanted.""",
            damage=25,
            durability=3  # Limited flares
        ),
        
        "harpoon": Weapon(
            "harpoon", 
            "Research Harpoon",
            """A specialized tool designed for collecting deep sea specimens. 
            It's been modified to defend against aggressive marine life.""",
            damage=15,
            durability=10
        ),
        
        "water_filter": Item(
            "water_filter",
            "Portable Water Filter",
            """A device designed to extract and purify water samples from the ocean. 
            Can analyze pollution levels and extract toxins from small water volumes."""
        ),
        
        "echo_sonar": Item(
            "echo_sonar",
            "Echo Sonar Device",
            """A handheld sonar that creates detailed 3D maps of the surrounding area. 
            Useful for navigation in dark or murky waters."""
        ),
        
        "bio_analyzer": Item(
            "bio_analyzer",
            "Biological Analyzer",
            """A compact device that can identify and analyze organic compounds, 
            measuring contamination levels in tissue samples."""
        )
    }
    return items

# Global item dictionary
ITEMS = initialize_items()

def get_item_by_id(item_id):
    """Get an item by its ID."""
    return ITEMS.get(item_id)