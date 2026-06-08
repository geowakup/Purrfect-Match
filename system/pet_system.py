from database import Database

class PetSystem:
    def __init__(self):
        self.db = Database()
        self.filename = "pet.json"

    # -------------------
    # GET PET DATA
    # -------------------
    def get_pet(self):
        pet = self.db.load(self.filename)

        # if no pet data, create default
        if pet is None:
            pet = {
                "food": 50,
                "happiness": 50
            }
            self.db.save(self.filename, pet)

        return pet

    # -------------------
    # SAVE PET DATA
    # -------------------
    def save_pet(self, pet):
        self.db.save(self.filename, pet)

    # -------------------
    # GIVE REWARD
    # -------------------
    def give_reward(self, food=5, happiness=3):
        pet = self.get_pet()

        pet["food"] += food
        pet["happiness"] += happiness

        self.save_pet(pet)

    # -------------------
    # DECAY (lose stats)
    # -------------------
    def decay(self):
        pet = self.get_pet()

        pet["food"] -= 1
        pet["happiness"] -= 1

        # prevent negative values
        if pet["food"] < 0:
            pet["food"] = 0
        if pet["happiness"] < 0:
            pet["happiness"] = 0

        self.save_pet(pet)