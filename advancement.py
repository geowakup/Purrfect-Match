import json
import os


class AdvancementsManager:
    def __init__(self, save_file=None):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.save_file = save_file or os.path.join(
            self.BASE_DIR,
            "data",
            "advancement.json"
        )
        self.legacy_save_file = os.path.join(
            self.BASE_DIR,
            "save_data.json"
        )

        self.advancements = {
            "first_launch": {
                "name": "🐣 First Launch",
                "unlocked": False,
                "reward": "Welcome bonus"
            },

            "feed_10": {
                "name": "🍖 Feed Pet 10 Times",
                "progress": 0,
                "goal": 10,
                "unlocked": False,
                "features": ["dark_theme", "river_flow"],
                "reward": "Unlock Dark Theme and River Flow"
            },

            "play_20": {
                "name": "🎮 Played 20 Actions",
                "progress": 0,
                "goal": 20,
                "unlocked": False,
                "features": ["bgm"],
                "reward": "Unlock BGM"
            },

            "alive_1_hour": {
                "name": "💤 Keep Pet Alive 1 Hour",
                "progress": 0,
                "goal": 3600,
                "unlocked": False,
                "features": ["developer_mode"],
                "reward": "Unlock Developer Mode"
            },

            "golden_finger": {
                "name": "👑 Unlock Golden Finger",
                "unlocked": False,
                "features": ["cyber_theme", "summer_ghost"],
                "reward": "Unlock Cyber Theme and Summer Ghost"
            },

            "unlock_bgm": {
                "name": "🎵 Unlock BGM",
                "unlocked": False,
                "features": ["bgm"],
                "reward": "Unlock BGM"
            },

            "unlock_dark_theme": {
                "name": "🌙 Unlock Dark Theme",
                "unlocked": False,
                "features": ["dark_theme"],
                "reward": "Unlock Dark Theme"
            },

            "unlock_cyber_theme": {
                "name": "💫 Unlock Cyber Theme",
                "unlocked": False,
                "features": ["cyber_theme"],
                "reward": "Unlock Cyber Theme"
            },

            "unlock_developer_mode": {
                "name": "🛠️ Unlock Developer Mode",
                "unlocked": False,
                "features": ["developer_mode"],
                "reward": "Unlock Developer Mode"
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

        if os.path.exists(self.legacy_save_file):
            try:
                os.remove(self.legacy_save_file)
            except OSError:
                pass

    # ------------------------
    # Load Data
    # ------------------------
    def load_data(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as file:
                self.advancements = json.load(file)

    # ------------------------
    # Sync unlocked features
    # ------------------------
    def sync_feature_unlocks(self):

        # reset all features
        for feature in self.feature_unlocks:
            self.feature_unlocks[feature] = False

        # enable features from unlocked achievements
        for advancement in self.advancements.values():

            if advancement.get("unlocked", False):

                for feature in advancement.get(
                    "features",
                    []
                ):
                    if feature in self.feature_unlocks:
                        self.feature_unlocks[feature] = True

    def has_feature_unlocked(self, feature_name):
        return self.feature_unlocks.get(feature_name, False)

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

            if data.get("unlocked", False):
                text += " ✅"
            else:
                text += " 🔒"

            reward = data.get("reward")
            if reward:
                text += f"\n   Reward: {reward}"

            lines.append(text)

        return "\n\n".join(lines)