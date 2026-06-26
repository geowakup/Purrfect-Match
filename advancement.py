import json
import os


class AdvancementsManager:
    def __init__(self, save_file=None):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.save_file = save_file or os.path.join(
            self.BASE_DIR,
            "data",
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
                "unlocked": False,
                "features": ["dark_theme"]
            },

            "play_20": {
                "name": "🎮 Played 20 Actions",
                "progress": 0,
                "goal": 20,
                "unlocked": False,
                "features": ["bgm"]
            },

            "alive_1_hour": {
                "name": "💤 Keep Pet Alive 1 Hour",
                "progress": 0,
                "goal": 3600,
                "unlocked": False,
                "features": ["developer_mode"]
            },

            "golden_finger": {
                "name": "👑 Unlock Golden Finger",
                "unlocked": False,
                "features": ["cyber_theme"]
            },

            "unlock_bgm": {
                "name": "🎵 Unlock BGM",
                "unlocked": False,
                "features": ["bgm"]
            },

            "unlock_dark_theme": {
                "name": "🌙 Unlock Dark Theme",
                "unlocked": False,
                "features": ["dark_theme"]
            },

            "unlock_cyber_theme": {
                "name": "💫 Unlock Cyber Theme",
                "unlocked": False,
                "features": ["cyber_theme"]
            },

            "unlock_developer_mode": {
                "name": "🛠️ Unlock Developer Mode",
                "unlocked": False,
                "features": ["developer_mode"]
            }
        }

        self.feature_unlocks = {
            "dark_theme": False,
            "cyber_theme": False,
            "bgm": False,
            "developer_mode": False
        }

        self.load_data()
        self.sync_feature_unlocks()

        # First launch unlock
        self.unlock("first_launch")

    # ------------------------
    # Unlock Achievement
    # ------------------------
    def unlock(self, key):
        if key not in self.advancements:
            return

        if not self.advancements[key]["unlocked"]:
            self.advancements[key]["unlocked"] = True

            for feature in self.advancements[key].get("features", []):
                self.feature_unlocks[feature] = True

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

        advancement["progress"] = round(advancement["progress"] + amount, 1)

        if advancement["progress"] >= advancement["goal"]:
            self.unlock(key)

        self.save_data()

    # ------------------------
    # Save Data
    # ------------------------
    def save_data(self):
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
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
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as file:
                loaded_data = json.load(file)

            merged_data = {}
            for key, default_advancement in self.advancements.items():
                if key not in loaded_data:
                    merged_data[key] = default_advancement.copy()
                    continue

                loaded_advancement = loaded_data[key]
                if not isinstance(loaded_advancement, dict):
                    merged_data[key] = default_advancement.copy()
                    continue

                merged_advancement = default_advancement.copy()
                merged_advancement.update(loaded_advancement)
                if "features" not in merged_advancement:
                    merged_advancement["features"] = default_advancement.get("features", [])
                merged_data[key] = merged_advancement

            self.advancements = merged_data

    def sync_feature_unlocks(self):
        self.feature_unlocks = {
            "dark_theme": False,
            "cyber_theme": False,
            "bgm": False,
            "developer_mode": False
        }

        for advancement in self.advancements.values():
            if advancement.get("unlocked", False):
                for feature in advancement.get("features", []):
                    self.feature_unlocks[feature] = True

    def has_feature_unlocked(self, feature):
        return self.feature_unlocks.get(feature, False)

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