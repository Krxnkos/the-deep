"""
Player module for The Deep game.
This is a reference file that imports the Player class from its actual location.
"""

import random  # Add missing import for random.randint

try:
    # Try importing from player package
    from player.player import Player
except ModuleNotFoundError:
    # Create a basic Player class definition if not found
    class Player:
        """Player class for the game."""
        def __init__(self, name):
            self.name = name
            self.health = 100
            self.max_health = 100
            self.inventory = []
            self.journal = []
            self.samples = []
            self.current_location = None  # Track current location
            self.equipped_weapon = None   # Track equipped weapon
            
        def attack(self):
            """Return damage for an attack, including weapon bonus"""
            base_damage = random.randint(5, 15)
            weapon_bonus = 0
            
            # Add weapon damage if equipped
            if self.equipped_weapon:
                weapon_bonus = self.equipped_weapon.damage_bonus
                
            return base_damage + weapon_bonus
            
        def show_inventory(self):
            """Return inventory as string"""
            if not self.inventory:
                return "Your inventory is empty."
            return "Inventory:\n" + "\n".join([f"- {item.name}" for item in self.inventory])
            
        def read_journal(self):
            """Return journal entries as string"""
            if not self.journal:
                return "Your journal is empty."
            return "Journal:\n" + "\n".join(self.journal)
            
        def view_samples(self):
            """Return collected samples as string"""
            if not self.samples:
                return "You haven't collected any samples yet."
            return "Samples:\n" + "\n".join([f"- {sample}" for sample in self.samples])
            
        def set_location(self, location):
            """Set the player's current location"""
            self.current_location = location
            
        def add_journal_entry(self, entry):
            """Add an entry to the player's journal"""
            self.journal.append(entry)
            return f"Added to journal: {entry}"
            
        def add_sample(self, sample_name):
            """Add a sample to the player's collection"""
            self.samples.append(sample_name)
            return f"Added sample: {sample_name}"
            
        def has_item(self, item_name):
            """Check if player has an item with the given name"""
            for item in self.inventory:
                if item.name.lower() == item_name.lower():
                    return True
            return False
            
        def get_item(self, item_name):
            """Get an item from inventory by name"""
            for item in self.inventory:
                if item.name.lower() == item_name.lower():
                    return item
            return None
            
        def remove_item(self, item_name):
            """Remove an item from inventory by name"""
            for i, item in enumerate(self.inventory):
                if item.name.lower() == item_name.lower():
                    return self.inventory.pop(i)
            return None
            
        def heal(self, amount):
            """Heal the player by the specified amount"""
            old_health = self.health
            self.health = min(self.health + amount, self.max_health)
            return self.health - old_health