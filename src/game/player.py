class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.current_location = None
        self.discovered_locations = []
        self.journal_entries = []
        self.samples_collected = []

    def take_damage(self, amount):
        """Take damage and return remaining health"""
        self.health -= amount
        if self.health < 0:
            self.health = 0
        return self.health
    
    def heal(self, amount):
        """Heal and return new health value"""
        self.health += amount
        if self.health > 100:
            self.health = 100
        return self.health
    
    def add_to_inventory(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
            return True
        else:
            print(f"Item '{item.name}' is already in inventory.")
            return False
    
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        else:
            print(f"Item '{item.name}' not found in inventory.")
            return False
        
    def show_inventory(self):
        if self.inventory:
            return "Inventory:\n" + "\n".join([item.name for item in self.inventory])
        else:
            return "Inventory is empty."
    
    def set_location(self, location):
        """Set player's current location and add to discovered locations"""
        self.current_location = location
        if location not in self.discovered_locations:
            self.discovered_locations.append(location)
    
    def add_journal_entry(self, entry):
        """Add a journal entry"""
        self.journal_entries.append(entry)
        print("New journal entry added.")
    
    def read_journal(self):
        """Read all journal entries"""
        if not self.journal_entries:
            return "Your journal is empty."
        
        return "Journal entries:\n\n" + "\n\n".join(self.journal_entries)
    
    def add_sample(self, sample_name, sample_data):
        """Add an environmental sample with analysis data"""
        sample = {
            "name": sample_name,
            "data": sample_data,
            "location": self.current_location
        }
        self.samples_collected.append(sample)
        print(f"Sample collected: {sample_name}")
        
    def view_samples(self):
        """View all collected environmental samples"""
        if not self.samples_collected:
            return "No samples collected yet."
            
        result = "Collected samples:\n"
        for sample in self.samples_collected:
            result += f"\n- {sample['name']}: {sample['data']}"
        
        return result

    def get_status(self):
        """Get complete player status"""
        return {
            "name": self.name,
            "health": self.health,
            "inventory": [item.name for item in self.inventory],
            "current_location": self.current_location,
            "discovered_locations": self.discovered_locations,
            "journal_entries": len(self.journal_entries),
            "samples_collected": len(self.samples_collected)
        }