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

        self.advancements = self._build_default_advancements()
        self.advancement_list = self._build_default_advancement_list()
        self.reward_callback = None

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

    def _build_default_advancements(self):
        return {
            "first_launch": {
                "name": "🐣 First Launch",
                "unlocked": False,
                "reward": "Welcome bonus"
            },

            "feed_pet": {
                "name": "🍖 Feed Pet 10 Times",
                "progress": 0,
                "goal": 10,
                "unlocked": False,
                "features": ["dark_theme"],
                "reward": "Unlock Dark Theme and Unlock Cyber Theme"
            },

            "click_pet": {
                "name": "👆 Click Pet",
                "progress": 0,
                "goal": 10,
                "unlocked": False,
                "features": ["river_flow"],
                "reward": "Unlock River Flow"
            },

            "buy_food": {
                "name": "🛒 Buy Food",
                "progress": 0,
                "goal": 10,
                "unlocked": False,
                "features": ["cyber_theme"],
                "reward": "Unlock Summer Ghost"
            },

            "play_for_1_hour": {
                "name": "🎮 Play for 1 Hour",
                "progress": 0,
                "goal": 3600,
                "unlocked": False,
                "features": ["summer_ghost"],
                "reward": "Unlock Developer Mode"
            },


            "unlock_dark_theme": {
                "name": "🌙 Unlock Dark Theme",
                "unlocked": False,
                "features": ["dark_theme"],
                "reward": "Get 100 Coins"
            },

            "unlock_cyber_theme": {
                "name": "💫 Unlock Cyber Theme",
                "unlocked": False,
                "features": ["cyber_theme"],
                "reward": "Get 100 Coins"
            },

            "unlock_developer_mode": {
                "name": "🛠️ Unlock Developer Mode",
                "unlocked": False,
                "features": ["developer_mode"],
                "reward": "Get 100 Coins"
            }
        }

    def _legacy_key_map(self):
        return {
            "feed_pet": "feed_10",
            "click_pet": "play_20",
            "play_for_1_hour": "alive_1_hour",
        }

    def _build_default_advancement_list(self):
        return [
            {
                "key": key,
                "name": data.get("name", key),
                "progress": data.get("progress", 0),
                "goal": data.get("goal"),
                "unlocked": data.get("unlocked", False),
                "features": list(data.get("features", [])),
                "reward": data.get("reward", ""),
            }
            for key, data in self._build_default_advancements().items()
        ]

    def _sync_advancement_list(self):
        self.advancement_list = []
        for key, data in self.advancements.items():
            self.advancement_list.append({
                "key": key,
                "name": data.get("name", key),
                "progress": data.get("progress", 0),
                "goal": data.get("goal"),
                "unlocked": data.get("unlocked", False),
                "features": list(data.get("features", [])),
                "reward": data.get("reward", ""),
            })

    def get_advancement_list(self):
        return [dict(item) for item in self.advancement_list]

    def get_advancement_by_key(self, key):
        for item in self.advancement_list:
            if item.get("key") == key:
                return dict(item)
        return None

    def add_advancement(self, key, name, goal=None, reward="", features=None, unlocked=False, progress=0):
        if key in self.advancements:
            return self.get_advancement_by_key(key)

        self.advancements[key] = {
            "name": name,
            "progress": progress,
            "goal": goal,
            "unlocked": unlocked,
            "features": list(features or []),
            "reward": reward,
        }
        self._sync_advancement_list()
        self.save_data()
        return self.get_advancement_by_key(key)

    def update_advancement(self, key, **updates):
        if key not in self.advancements:
            return None

        for field, value in updates.items():
            if field == "features" and value is not None:
                self.advancements[key][field] = list(value)
            else:
                self.advancements[key][field] = value

        self._sync_advancement_list()
        self.save_data()
        return self.get_advancement_by_key(key)

    def get_unlocked_advancements(self):
        return [item for item in self.get_advancement_list() if item.get("unlocked", False)]

    def get_locked_advancements(self):
        return [item for item in self.get_advancement_list() if not item.get("unlocked", False)]

    def sync_feature_unlocks(self):
        self.feature_unlocks = {
            "dark_theme": False,
            "cyber_theme": False,
            "bgm": False,
            "developer_mode": False,
            "river_flow": False,
            "summer_ghost": False,
        }

        for key, advancement in self.advancements.items():
            if not advancement.get("unlocked", False):
                continue

            for feature in advancement.get("features", []):
                self.feature_unlocks[feature] = True

    def has_feature_unlocked(self, feature_name):
        return self.feature_unlocks.get(feature_name, False)

    # ------------------------
    # Unlock Achievement
    # ------------------------
    def unlock(self, key):
        if key not in self.advancements:
            return

        if not self.advancements[key].get("unlocked", False):
            self.advancements[key]["unlocked"] = True

            for feature in self.advancements[key].get("features", []):
                if feature in self.feature_unlocks:
                    self.feature_unlocks[feature] = True

            self._sync_advancement_list()
            self.sync_feature_unlocks()
            print(
                f"Advancement unlocked: "
                f"{self.advancements[key]['name']}"
            )

            reward = self.advancements[key].get("reward", "")
            if "100 coins" in reward.lower() and self.reward_callback is not None:
                self.reward_callback(100)

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

        self._sync_advancement_list()
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
        defaults = self._build_default_advancements()

        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as file:
                loaded = json.load(file)

            merged = {}
            for key, default_value in defaults.items():
                saved_value = loaded.get(key)
                if saved_value is not None:
                    merged[key] = {**default_value, **saved_value}
                    continue

                legacy_key = self._legacy_key_map().get(key)
                old_value = loaded.get(legacy_key)
                if old_value is None:
                    merged[key] = default_value
                    continue

                old_progress = old_value.get("progress", 0)
                old_goal = old_value.get("goal", 1)
                new_goal = default_value.get("goal", 1)
                if old_goal > 0:
                    preserved_progress = round((old_progress / old_goal) * new_goal, 1)
                else:
                    preserved_progress = 0

                merged[key] = {
                    **default_value,
                    "progress": min(preserved_progress, new_goal),
                    "unlocked": old_value.get("unlocked", False),
                }

            self.advancements = merged
        else:
            self.advancements = defaults

        self._sync_advancement_list()

    def clear_saved_state(self):
        for path in [self.save_file, self.legacy_save_file]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass

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