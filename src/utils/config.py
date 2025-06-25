# Configuration settings for The Deep game
class Config:
    """Configuration settings for The Deep game."""
    
    # Window settings
    WINDOW_TITLE = "The Deep"
    WINDOW_WIDTH = 80
    WINDOW_HEIGHT = 25

    # Game settings
    DEBUG_MODE = False
    SAVE_DIRECTORY = "saves"
    
    # UI settings
    TEXT_SPEED = 0.03  # seconds per character for text animation
    TITLE_COLOR = "cyan"
    TEXT_COLOR = "white"
    WARNING_COLOR = "yellow"
    DANGER_COLOR = "red"
    
    # Audio settings (for future implementation)
    SOUND_ENABLED = True
    MUSIC_VOLUME = 0.7
    EFFECTS_VOLUME = 1.0
    
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

    DEFAULT_DIFFICULTY = 'normal'
    SAVE_FILE_PATH = 'saves/save_data.json'
    ASSETS_PATH = 'resources/ascii/'

    @staticmethod
    def get_version():
        return "0.1.0"