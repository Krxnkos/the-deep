# Contents of /the-deep-adventure/the-deep-adventure/src/story/endings.py

class Endings:
    def __init__(self):
        self.endings = {
            "good": "You successfully navigate the treacherous depths, uncovering the truth behind the Abyssal Scanner and the corrupted coral. With the knowledge gained, you manage to save the ocean from impending doom, restoring balance to the ecosystem. As you resurface, the sun breaks through the clouds, illuminating the waters with hope.",
            "bad": "In your quest for knowledge, you succumb to the madness that lurks in the depths. The voices of the ocean consume you, and you become a part of the very horror you sought to understand. Your fate is sealed as you drift into the abyss, lost to the world above.",
            "neutral": "You uncover fragments of the truth but are unable to piece them together. The ocean remains a mystery, and while you escape with your life, the haunting whispers of the deep follow you. You return to the surface, forever changed, but with more questions than answers.",
            "sacrifice": "In a moment of clarity, you realise that to save the ocean, a sacrifice must be made. You choose to stay behind, confronting the Tidecaller and accepting your fate. Your bravery inspires others to protect the ocean, and your story becomes a legend among those who dare to explore the depths."
        }

    def get_ending(self, ending_type):
        return self.endings.get(ending_type, "Unknown ending.")