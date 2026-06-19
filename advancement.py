import json
import os


class AdvancementsManager:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.save_file = os.path.join(
            self.BASE_DIR,
            "advancements.json"
        )

        self.advancements = {
            "first_launch": {
                "name": "🐣 First Launch",
                "unlocked": False
            },

            "feed_10": {
                "name": "🍖 Feed Pet 10 Times",
                "progress": 0,
                "goal": 10,
                "unlocked": False
            },

            "play_20": {
                "name": "🎮 Played 20 Actions",
                "progress": 0,
                "goal": 20,
                "unlocked": False
            },

            "alive_1_hour": {
                "name": "💤 Keep Pet Alive 1 Hour",
                "progress": 0,
                "goal": 3600,
                "unlocked": False
            },

            "golden_finger": {
                "name": "👑 Unlock Golden Finger",
                "unlocked": False
            }
        }

        self.load_data()

        # First launch unlock
        self.unlock("first_launch")

    # ------------------------
    # Unlock Achievement
    # ------------------------
    def unlock(self, key):

        if key not in self.advancements:

            print(
                "Missing advancement:",
                key
            )

            return

        if not self.advancements[key]["unlocked"]:

            self.advancements[key]["unlocked"] = True

            print(
                f"Advancement unlocked: "
                f"{self.advancements[key]['name']}"
            )

            self.save_data()

    # ------------------------
    # Add Progress
    # ------------------------
    def add_progress(self, key, amount=1):
        advancement = self.advancements[key]

        if advancement["unlocked"]:
            return

        advancement["progress"] =advancement["progress"] = round(advancement["progress"] + amount,1)

        if advancement["progress"] >= advancement["goal"]:
            self.unlock(key)

        self.save_data()

    # ------------------------
    # Save Data
    # ------------------------
    def save_data(self):
        with open(self.save_file, "w") as file:
            json.dump(
                self.advancements,
                file,
                indent=4
            )

    # ------------------------
    # Load Data
    # ------------------------
    def load_data(self):

        if not os.path.exists(
            self.save_file
        ):
            return

        try:

            with open(
                self.save_file,
                "r"
            ) as file:

                loaded = json.load(file)

            for key in loaded:

                if key in self.advancements:

                    self.advancements[key].update(
                        loaded[key]
                    )

        except Exception as e:

            print(
                "Advancement load error:",
                e
            )
    # ------------------------
    # Get List
    # ------------------------
    def get_advancement_text(self):
        lines = []

        for data in self.advancements.values():

            if "goal" in data:
                text = (
                    f"{data['name']} "
                    f"({data['progress']}/"
                    f"{data['goal']})"
                )
            else:
                text = data["name"]

            if data["unlocked"]:
                text += " ✅"

            lines.append(text)

        return "\n".join(lines)