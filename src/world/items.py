"""
Items for The Deep game.
Defines the items, their properties, and their effects.
"""

from game.player import Player

class Item:
    def __init__(self, item_id, name, description, usable=False, on_pickup_message=None, consumable=False):
        self.id = item_id
        self.name = name
        self.description = description
        self.usable = usable
        self.on_pickup_message = on_pickup_message
        self.consumable = consumable
        
    def use(self, player, location=None):
        """Default use method, should be overridden by specific items"""
        if not self.usable:
            return f"You can't use the {self.name} here."
        return f"You used the {self.name}, but nothing happened."

class HealingItem(Item):
    def __init__(self, item_id, name, description, heal_amount, on_pickup_message=None):
        super().__init__(item_id, name, description, usable=True, on_pickup_message=on_pickup_message, consumable=True)
        self.heal_amount = heal_amount
        
    def use(self, player, location=None):
        """Use the healing item to restore health"""
        if player.health >= player.max_health:
            return f"You are already at full health."
            
        old_health = player.health
        player.health = min(player.health + self.heal_amount, player.max_health)
        
        return f"You used the {self.name} and recovered {player.health - old_health} health points."

class SampleContainer(Item):
    def __init__(self, item_id, name, description, on_pickup_message=None):
        super().__init__(item_id, name, description, usable=True, on_pickup_message=on_pickup_message, consumable=True)
        
    def use(self, player, location=None):
        """Use the sample container to collect a sample from the environment"""
        sample_name = f"Sample from {location.name if location else 'Unknown Location'}"
        player.samples.append(sample_name)
        return f"You used the {self.name} to collect a {sample_name}."

class WeaponItem(Item):
    """Weapon item that enhances player attack damage"""
    def __init__(self, item_id, name, description, damage_bonus, on_pickup_message=None, consumable=False):
        super().__init__(item_id, name, description, usable=True, on_pickup_message=on_pickup_message, consumable=consumable)
        self.damage_bonus = damage_bonus
        self.equipped = False
        
    def use(self, player, location=None):
        """Equip/unequip the weapon"""
        # Check if player has a weapon equipped attribute, add if not
        if not hasattr(player, 'equipped_weapon'):
            player.equipped_weapon = None
            
        if player.equipped_weapon == self:
            # Unequip the weapon
            player.equipped_weapon = None
            self.equipped = False
            return f"You put away the {self.name}."
        else:
            # Unequip current weapon if any
            if player.equipped_weapon:
                player.equipped_weapon.equipped = False
                
            # Equip this weapon
            player.equipped_weapon = self
            self.equipped = True
            return f"You equipped the {self.name}, increasing your attack damage by {self.damage_bonus}."

# Initialize all items in the game
_ITEMS = {
    # Basic equipment
    "binoculars": Item("binoculars", "Binoculars", "Standard binoculars for observing distant objects.", usable=True),
    "oxygen_tank": Item("oxygen_tank", "Oxygen Tank", "An auxiliary oxygen tank for deep dives.", usable=True),
    
    # Samples and research items
    "water_sample": Item("water_sample", "Water Sample", "A sample of water from the reef area.", usable=False),
    "plastic_sample": Item("plastic_sample", "Plastic Debris Sample", "A sample of microplastic pollution.", usable=False),
    "chemical_sample": Item("chemical_sample", "Chemical Waste Sample", "A vial containing unidentified chemical waste.", usable=False),
    "thermal_sample": Item("thermal_sample", "Thermal Vent Sample", "A sample of mineral-rich water from a hydrothermal vent.", usable=False),
    "pressure_sample": Item("pressure_sample", "Deep Pressure Sample", "A specially designed container holding water from extreme depths.", usable=False),
    "sample_vial": SampleContainer("sample_vial", "Sample Vial", "A sterile container for collecting biological samples.", on_pickup_message="You can use this to collect samples for research."),
    
    # Health items
    "medkit": HealingItem("medkit", "Medical Kit", "A waterproof first-aid kit designed for marine expeditions.", 50, "This will be useful if you get injured."),
    
    # Story items
    "research_log": Item("research_log", "Dr. Elson's Research Log", "A tablet containing research data from Dr. Mira Elson.", usable=True),
    "strange_artifact": Item("strange_artifact", "Strange Artifact", "An object of unknown origin with peculiar markings.", usable=True),
    "mutated_coral": Item("mutated_coral", "Mutated Coral Sample", "A piece of coral showing signs of unusual growth patterns.", usable=False),
    "elson_final_notes": Item("elson_final_notes", "Dr. Elson's Final Notes", "The last recorded observations of Dr. Elson regarding 'The Awakening'.", usable=True),
    "tidecaller_essence": Item("tidecaller_essence", "Tidecaller Essence", "A strange, pulsating substance that seems to be connected to the ocean itself.", usable=True),
    
    # Additional healing items
    "small_medkit": HealingItem(
        "small_medkit", 
        "Small First Aid Kit", 
        "A small kit with basic first aid supplies.", 
        25, 
        "A basic first aid kit that could help with minor injuries."
    ),
    "large_medkit": HealingItem(
        "large_medkit", 
        "Advanced Medical Kit",
        "A comprehensive medical kit with advanced treatments.",
        75,
        "This advanced medical kit could save your life in dangerous situations."
    ),
    "stim_pack": HealingItem(
        "stim_pack",
        "Emergency Stimulant",
        "A fast-acting emergency medical stimulant.",
        40,
        "For emergency use only. Rapidly boosts recovery but with potential side effects."
    ),
    "healing_gel": HealingItem(
        "healing_gel",
        "Bio-Regenerative Gel",
        "Advanced gel that accelerates natural healing processes.",
        30,
        "The latest in bio-regenerative technology. Apply directly to wounds."
    ),
    
    # Weapons
    "dive_knife": WeaponItem(
        "dive_knife",
        "Diving Knife",
        "A standard diving knife with a serrated edge.",
        5,
        "A basic tool for divers, but can also be used for self-defense."
    ),
    "harpoon_gun": WeaponItem(
        "harpoon_gun",
        "Harpoon Gun",
        "A compact underwater harpoon gun with limited range.",
        15,
        "Designed for underwater hunting and self-defense."
    ),
    "sonic_disruptor": WeaponItem(
        "sonic_disruptor",
        "Sonic Disruptor",
        "An experimental device that emits targeted sonic waves.",
        20,
        "This prototype weapon disrupts the nervous system of marine predators."
    ),
    "plasma_cutter": WeaponItem(
        "plasma_cutter",
        "Plasma Cutting Tool",
        "An industrial tool that generates a focused plasma arc.",
        25,
        "Designed for cutting through metal, but dangerous in combat too."
    )
}

def get_item_by_id(item_id):
    """Get an item instance by its ID."""
    item = _ITEMS.get(item_id.lower())
    if not item:
        return None
    return item