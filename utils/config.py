# Configuration settings for the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Difficulty levels
DIFFICULTY_LEVELS = {
    'easy': {
        'enemy_damage_multiplier': 0.5,
        'resource_spawn_rate': 1.5,
    },
    'normal': {
        'enemy_damage_multiplier': 1.0,
        'resource_spawn_rate': 1.0,
    },
    'hard': {
        'enemy_damage_multiplier': 1.5,
        'resource_spawn_rate': 0.75,
    },
}

# Game settings
DEFAULT_DIFFICULTY = 'normal'
SAVE_FILE_PATH = 'saves/save_data.json'
ASSETS_PATH = 'resources/ascii/'