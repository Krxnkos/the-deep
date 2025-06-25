class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.current_location = None

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
    
    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
    
    def add_to_inventory(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
        else:
            print(f"Item '{item}' is already in inventory.")
    
    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
        else:
            print(f"Item '{item}' not found in inventory.")
        
    def show_inventory(self):
        if self.inventory:
            return "Inventory:\n" + "\n".join(self.inventory)
        else:
            print("Inventory is empty.")
    
    def set_location(self, location):
        self.current_location = location

    def get_status(self):
        return {
            "name": self.name,
            "health": self.health,
            "inventory": self.inventory,
            "current_location": self.current_location
        }