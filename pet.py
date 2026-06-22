import random

class Pet:
    def __init__(self, name="Pet"):

        # Core attributes
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.cleanliness = 50

        # GUI state system
        self.state = "happy"
        self.action = None
        self.action_timer = 0

        self.coins = 100
        self.inventory = []

        self.alive = True
        self.age = 0

    # -------------------------
    # STATE SYSTEM
    # -------------------------
    def update_state(self):

        # Action overrides mood
        if self.action is not None:
            self.state = self.action
            return

        # Mood priority system
        if self.hunger < 40:
            self.state = "starving"
        elif self.hunger <= 60:
            self.state = "hungry"
        elif self.energy <= 20:
            self.state = "sleepy"
        elif self.cleanliness <= 20:
            self.state = "dirty"
        elif self.happiness <= 30:
            self.state = "sad"
        else:
            self.state = "happy"

    # -------------------------
    # RANDOM ACTIONS
    # -------------------------
    def trigger_random_action(self):
        self.action = random.choice(["jump", "roll", "sleep"])
        self.action_timer = 10

    # -------------------------
    # INTERACTIONS
    # -------------------------
    def feed(self):
        self.hunger = min(100, self.hunger + 15)
        self.update_state()

    def play(self):
        self.happiness = min(100, self.happiness + 10)
        self.energy = max(0, self.energy - 5)
        self.update_state()

    def rest(self):
        self.energy = min(100, self.energy + 15)
        self.update_state()

    def clean(self):
        self.cleanliness = min(100, self.cleanliness + 20)
        self.update_state()

    # -------------------------
    # MAIN UPDATE LOOP
    # -------------------------
    def update(self):

        print("Pet update running")

        # Decay stats
        self.hunger = max(0, self.hunger - 1)
        self.energy = max(0, self.energy - 1)
        self.cleanliness = max(0, self.cleanliness - 1)

        # Happiness decay
        if self.hunger <= 30 or self.energy <= 30:
            self.happiness = max(0, self.happiness - 1)

        # Action timer (don't decrement in developer mode - indicated by high value)
        if self.action_timer < 1000:  # Only decrement normal timers, not developer mode
            if self.action_timer > 0:
                self.action_timer -= 1
            else:
                self.action = None

        self.update_state()

    # -------------------------
    # STATUS FOR GUI
    # -------------------------
    def status(self):
        return {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "cleanliness": self.cleanliness,
            "state": self.state,
            "action": self.action,
            "coin": self.coins,
            "inventory": self.inventory, 
        }
    
# =========================
# TEST
# =========================
if __name__ == "__main__":

    pet = Pet()

    print("Pet class is working!")
    print(pet.status())

    pet.feed()

    print("After feeding:")
    print(pet.status())