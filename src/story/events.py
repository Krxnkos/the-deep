# events.py

import random

class Event:
    def __init__(self, description, consequences):
        self.description = description
        self.consequences = consequences

    def trigger(self, player):
        print(self.description)
        for consequence in self.consequences:
            consequence.apply(player)

class Consequence:
    def __init__(self, change_type, amount):
        self.change_type = change_type
        self.amount = amount

    def apply(self, player):
        if self.change_type == 'health':
            player.health += self.amount
            print(f"Your health has been {'increased' if self.amount > 0 else 'decreased'} by {abs(self.amount)}.")
        elif self.change_type == 'inventory':
            player.inventory.append(self.amount)
            print(f"You have acquired: {self.amount}.")
        elif self.change_type == 'mental_state':
            player.mental_state += self.amount
            print(f"Your mental state has {'improved' if self.amount > 0 else 'deteriorated'}.")

def generate_random_event():
    events = [
        Event("You find a strange glowing coral that whispers secrets of the deep.", 
              [Consequence('mental_state', 1)]),
        Event("A sudden surge of water knocks you off balance, causing minor injuries.", 
              [Consequence('health', -10)]),
        Event("You encounter a ghostly figure that offers you a choice: take a risk or retreat.", 
              [Consequence('mental_state', -2), Consequence('inventory', 'Diver’s Talisman')]),
        Event("You discover an emergency flare gun hidden in the debris.", 
              [Consequence('inventory', 'Emergency Flare Gun')]),
        Event("A hallucination causes you to lose track of time, affecting your progress.", 
              [Consequence('mental_state', -3)]),
    ]
    return random.choice(events)