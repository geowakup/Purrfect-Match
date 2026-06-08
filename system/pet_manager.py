import time

class Pet:
    def __init__(self, name="Buddy"):
        self.name = name

        # Core stats (0–100)
        self.hunger = 100
        self.happiness = 100
        self.energy = 100

        # State
        self.mood = "happy"

        # Last update time (for decay system)
        self.last_update = time.time()

    # -------------------------
    # BASIC UPDATE SYSTEM
    # -------------------------
    def update(self):
        """Apply time-based decay to stats. Call regularly."""
        now = time.time()
        elapsed = now - self.last_update

        # Decay rates per second
        hunger_decay = 0.05 * elapsed
        energy_decay = 0.03 * elapsed
        happiness_decay = 0.02 * elapsed

        self.hunger = max(0, self.hunger - hunger_decay)
        self.energy = max(0, self.energy - energy_decay)
        self.happiness = max(0, self.happiness - happiness_decay)

        self.last_update = now
        self.update_mood()

    # -------------------------
    # MOOD SYSTEM
    # -------------------------
    def update_mood(self):
        """Update mood based on current stats."""
        if self.hunger < 20:
            self.mood = "starving"
        elif self.energy < 20:
            self.mood = "sleeping"
        elif self.happiness < 30:
            self.mood = "sad"
        elif self.hunger > 70 and self.happiness > 70:
            self.mood = "happy"
        else:
            self.mood = "idle"

    # -------------------------
    # FEEDING SYSTEM
    # -------------------------
    def feed(self, food_value=20):
        """Feed the pet to restore hunger and slightly boost happiness."""
        self.hunger = min(100, self.hunger + food_value)
        self.happiness = min(100, self.happiness + 5)
        self.update_mood()

    # -------------------------
    # PLAY / BOOST SYSTEM
    # -------------------------
    def play(self):
        """Play with the pet to increase happiness but reduce energy."""
        self.happiness = min(100, self.happiness + 15)
        self.energy = max(0, self.energy - 10)
        self.update_mood()

    # -------------------------
    # ENERGY REST SYSTEM
    # -------------------------
    def sleep(self):
        """Let the pet sleep to restore energy but slightly reduce hunger."""
        self.energy = min(100, self.energy + 30)
        self.hunger = max(0, self.hunger - 5)
        self.update_mood()

    # -------------------------
    # GET STATE (for UI / database)
    # -------------------------
    def get_state(self):
        """Return current pet state as a dictionary."""
        return {
            "name": self.name,
            "hunger": round(self.hunger, 2),
            "happiness": round(self.happiness, 2),
            "energy": round(self.energy, 2),
            "mood": self.mood,
        }
