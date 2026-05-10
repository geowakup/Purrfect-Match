import random

class Pet:
    def __init__ (self, name: str):
        # Core attributes
        self.name = name
        self.hunger = 100          # 0 = starving, 100 = full
        self.happiness = 100    # 0 = sad, 100 =happy
        self.energy = 100          # 0 = exhausted, 100 = energetic 
        self.cleanliness = 100       # 0 = dirty, 100 = clean

        self.state = {
            "mood": "happy",
            "action": None
        }                            # idle, happy, sad, sleeping 

        self.action_timer = 0

    # --- State Updates ---
    def update_state(self):
        if self.hunger <= 20:
            self.state["mood"] = "starving"

        elif self.cleanliness <= 20:
            self.state["mood"] = "dirty"

        elif self.energy <= 20:
            self.state["mood"] = "sleepy"

        elif self.hunger >= 80:
            self.state["mood"] = "full"

        elif self.happiness <= 20:
            self.state["mood"] = "sad"

        elif self.happiness >= 80:
            self.state["mood"] = "happy"

        elif self.energy >= 80:
            self.state["mood"] = "energetic"

        else:
            self.state["mood"] = "idle"

    # --- RANDOM ACTION ---
    def trigger_random_action(self):
        self.state["action"] = random.choice(["jump", "roll", "sleep"])
        self.action_timer = 10


    def status(self):
        return{
            "name" : self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "energy": self.energy,
            "cleanliness": self.cleanliness,
            "mood": self.state["mood"],
            "action": self.state["action"]
        }

    # --- User Interactions ---
    def feed(self):
        """Feed the pet to increase hunger level."""
        self.hunger = min(100, self.hunger + 10)
        self.update_state()

    def play(self):
        """Play with the pet to increase happiness and reduce energy."""
        self.happiness = min(100, self.happiness + 10)
        self.energy = max(0, self.energy - 5)
        self.update_state()

    def rest(self):
        """Let the pet rest to restore energy."""
        self.energy = min(100, self.energy + 15)
        self.update_state()

    def clean(self):
        """Clean the pet to restore cleanliness."""
        self.cleanliness = min(100, self.cleanliness + 20)
        self.update_state()

    #--- Update Loop ---#
    def update(self):
        # Stat decay
        self.hunger = max(0, self.hunger -1)
        self.happiness = max(0, self.happiness -1)
        self.energy = max(0, self.energy -1)
        self.cleanliness = max(0, self.cleanliness -1)
        
        # temporary action
        if self.action_timer > 0:
            self.action_timer -= 1
        else:
            self.state["action"] = None
            return
        
        # state logic
        self.update_state() 