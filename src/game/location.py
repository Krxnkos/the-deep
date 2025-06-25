# This file might need to be created or modified

class Location:
    def __init__(self, location_id, name, description):
        self.id = location_id
        self.name = name
        self.description = description
        self.exits = {}  # Dictionary mapping directions to location IDs
        self.items = []  # List of items in this location
    
    def add_exit(self, direction, location_id):
        """Add an exit from this location."""
        self.exits[direction] = location_id
    
    def remove_exit(self, direction):
        """Remove an exit from this location."""
        if direction in self.exits:
            del self.exits[direction]
    
    def add_item(self, item):
        """Add an item to this location."""
        self.items.append(item)
    
    def remove_item(self, item):
        """Remove an item from this location."""
        if item in self.items:
            self.items.remove(item)
