# =========================
# save_system.py
# =========================

import json
import os


class SaveSystem:

    def __init__(self, filename="save_data.json"):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.data_folder = os.path.join(self.BASE_DIR, "data")
        os.makedirs(self.data_folder, exist_ok=True)
        self.filename = os.path.join(self.data_folder, filename)

    # =========================
    # SAVE
    # =========================
    def save_pet(self, pet, character):

        data = {

            "name": pet.name,
            "hunger": pet.hunger,
            "happiness": pet.happiness,
            "energy": pet.energy,
            "cleanliness": pet.cleanliness,

            "state": pet.state,
            "action": pet.action,

            "alive": pet.alive,
            "age": pet.age,

            "coins": pet.coins,
            "inventory": pet.inventory,

            "character": character
        }

        with open(self.filename, "w") as file:

            json.dump(data, file, indent=4)

        print("Pet saved!")

    # =========================
    # LOAD
    # =========================
    def load_pet(self, pet):

        if not os.path.exists(self.filename):

            print("No save file found.")

            return None

        with open(self.filename, "r") as file:

            data = json.load(file)

        print (data)
        pet.name = data.get("name", "Firefly")
        pet.hunger = data["hunger"]
        pet.happiness = data["happiness"]
        pet.energy = data["energy"]
        pet.cleanliness = data["cleanliness"]

        pet.state = data["state"]
        pet.action = data["action"]

        pet.alive = data["alive"]
        pet.age = data["age"]
        pet.character = data["character"]

        pet.coins = data.get("coins", 100)
        pet.inventory = data.get("inventory", [])
        print("Pet loaded!")

        return data["character"]