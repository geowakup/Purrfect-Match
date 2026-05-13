from pet import Pet
import random

class Pet:
    def __init__(self, name="Pet"):

        # Core attributes
        self.name = name
        self.hunger = 100
        self.happiness = 100
        self.energy = 100
        self.cleanliness = 100

        # GUI-compatible state system
        self.state = "happy"
        self.action = None
        self.action_timer = 0

    # -------------------------
    # STATE SYSTEM
    # -------------------------
    def update_state(self):

        # If performing action, override mood
        if self.action is not None:
            self.state = self.action
            return

        # Priority-based mood logic
        if self.hunger <= 20:
            self.state = "starving"
        elif self.hunger <= 40:
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
    # RANDOM ACTION SYSTEM
    # -------------------------
    def trigger_random_action(self):
        self.action = random.choice(["jump", "roll", "sleep"])
        self.action_timer = 10

    # -------------------------
    # USER INTERACTIONS
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
    # UPDATE LOOP (TICK)
    # -------------------------
    def update(self):

        # Stat decay
        self.hunger = max(0, self.hunger - 1)
        self.energy = max(0, self.energy - 1)
        self.cleanliness = max(0, self.cleanliness - 1)

        # Conditional happiness decay
        if self.hunger <= 30 or self.energy <= 30:
            self.happiness = max(0, self.happiness - 1)

        # Action timer system
        if self.action_timer > 0:
            self.action_timer -= 1
        else:
            self.action = None

        # Update final state
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
            "action": self.action
        }