class Dialogue:
    def __init__(self):
        self.dialogues = {
            "intro": [
                "You awaken in the dimly lit research station, the sound of water dripping echoing around you.",
                "A voice whispers from the shadows, 'Welcome to Erebus-9. Are you ready to uncover the truth?'"
            ],
            "mira": [
                "Dr. Mira Elson appears in a flickering vision.",
                "'You must understand, the ocean holds secrets that can drive a person mad...'",
                "'Trust your instincts, but beware of what lies beneath.'"
            ],
            "captain": [
                "Captain Theo Nash stands before you, his eyes haunted.",
                "'I've seen things down there... things that should not exist.'",
                "'We need to keep our wits about us, or we may not return.'"
            ],
            "echo": [
                "The AI, Echo, crackles to life.",
                "'Analyzing... Warning: Anomalies detected in your vicinity.'",
                "'Proceed with caution. Trust is a fragile concept.'"
            ],
            "tidecaller": [
                "A chilling voice resonates through your mind.",
                "'I am the Tidecaller, the embodiment of the ocean's wrath.'",
                "'You cannot escape your fate, nor the consequences of your actions.'"
            ]
        }

    def get_dialogue(self, character):
        return self.dialogues.get(character, ["No dialogue available."])

    def display_dialogue(self, character):
        dialogue_lines = self.get_dialogue(character)
        for line in dialogue_lines:
            print(line)
            input("Press Enter to continue...")  # Wait for user input to proceed

# Example usage:
if __name__ == "__main__":
    dialogue_system = Dialogue()
    dialogue_system.display_dialogue("intro")
    dialogue_system.display_dialogue("mira")
    dialogue_system.display_dialogue("captain")
    dialogue_system.display_dialogue("echo")
    dialogue_system.display_dialogue("tidecaller")