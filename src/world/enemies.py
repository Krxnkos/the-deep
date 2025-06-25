import random

class Enemy:
    """Base class for all enemies in the game."""
    def __init__(self, id, name, description, health, damage, loot=None, attack_range=(5, 15), threat_level=0.5):
        self.id = id
        self.name = name
        self.description = description
        self.max_health = health
        self.health = health
        self.damage = damage
        self.loot = loot or []  # List of possible item IDs to drop
        self.attack_min, self.attack_max = attack_range
        self.threat_level = threat_level  # Add this attribute (0.0 to 1.0)
    
    def attack(self):
        """Return damage for an attack"""
        return random.randint(self.attack_min, self.attack_max)
    
    def take_damage(self, amount):
        """Enemy takes damage"""
        self.health -= amount
        if self.health < 0:
            self.health = 0
        
        if self.health == 0:
            return f"The {self.name} has been defeated!"
        elif self.health < self.max_health / 4:
            return f"The {self.name} is severely injured!"
        elif self.health < self.max_health / 2:
            return f"The {self.name} appears wounded!"
        else:
            return f"The {self.name} flinches from the attack!"
    
    def is_alive(self):
        """Check if enemy is still alive"""
        return self.health > 0
    
    def get_loot(self):
        """Get random loot from enemy"""
        if not self.loot:
            return None
        return random.choice(self.loot)
    
    def describe(self):
        """Get enemy description with health status"""
        health_status = "healthy"
        health_percent = (self.health / self.max_health) * 100
        
        if health_percent <= 25:
            health_status = "critically injured"
        elif health_percent <= 50:
            health_status = "wounded"
        elif health_percent <= 75:
            health_status = "slightly injured"
            
        return f"{self.description}\n\nIt appears {health_status}."

# Define enemy types
def initialize_enemies():
    enemies = {
        "mutated_angler": Enemy(
            "mutated_angler",
            "Mutated Angler Fish",
            """A grotesquely enlarged angler fish with multiple bioluminescent lures. Its body is 
            covered in tumor-like growths and its teeth are unnaturally elongated. Chemical waste 
            has clearly altered its natural biology.""",
            health=50,
            damage=15,
            loot=["fish_tissue"]
        ),
        
        "plastic_kraken": Enemy(
            "plastic_kraken",
            "Plastic Entangled Squid",
            """A giant squid whose body has become fused with plastic waste. Fishing nets, plastic bags, 
            and bottles are embedded in its flesh. It moves erratically, clearly in pain and confused.""",
            health=75,
            damage=20,
            loot=["plastic_sample", "squid_tissue"]
        ),
        
        "bloom_stalker": Enemy(
            "bloom_stalker",
            "Bloom Stalker",
            """A humanoid figure composed of the black kelp from the Bloom. Its form is constantly 
            shifting and reassembling, with glowing red spots where eyes might be located.""",
            health=100,
            damage=25,
            loot=["corrupted_tissue"]
        ),
        
        "chemical_crawler": Enemy(
            "chemical_crawler",
            "Chemical Crawler",
            """A crab-like creature with a shell partially dissolved by chemical exposure. 
            Its claws drip with caustic fluid, and it has adapted to use industrial waste as armor.""",
            health=40,
            damage=30,
            loot=["chemical_sample"]
        ),
        
        "ghost_shoal": Enemy(
            "ghost_shoal",
            "Ghost Shoal",
            """A swarm of skeletal fish that move as one entity. Their bones are bleached white 
            from chemical exposure, and they emit a faint blue phosphorescence.""",
            health=60,
            damage=15,
            loot=["bone_fragment"]
        ),
        
        "tidecaller_avatar": Enemy(
            "tidecaller_avatar",
            "Tidecaller's Avatar",
            """A towering figure formed of water, debris, and marine life. It appears to be a 
            manifestation of the ocean's wrath, constantly changing form but retaining a vaguely 
            humanoid shape.""",
            health=200,
            damage=35,
            loot=["tidecaller_essence"]
        )
    }
    return enemies

# Enemy spawn configuration per location
ENEMY_SPAWNS = {
    "erebus9": ["chemical_crawler"],
    "trench": ["mutated_angler", "ghost_shoal"],
    "ghost_reef": ["ghost_shoal", "plastic_kraken"],
    "fishing_trawler": ["mutated_angler", "chemical_crawler"],
    "black_bloom": ["bloom_stalker", "tidecaller_avatar"]
}

def get_random_enemy_for_location(location_id):
    """Get a random enemy type appropriate for the given location"""
    if location_id not in ENEMY_SPAWNS:
        return None
    
    enemy_types = ENEMY_SPAWNS[location_id]
    if not enemy_types:
        return None
        
    enemy_id = random.choice(enemy_types)
    enemies = initialize_enemies()
    
    if enemy_id in enemies:
        return Enemy(
            enemies[enemy_id].id,
            enemies[enemy_id].name,
            enemies[enemy_id].description,
            enemies[enemy_id].max_health,
            enemies[enemy_id].damage,
            enemies[enemy_id].loot
        )
    
    return None