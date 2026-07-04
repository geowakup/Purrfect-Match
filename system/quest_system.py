from system.database import Database
from datetime import date
import random


class QuestSystem:
    """A daily quest system backed by `Database`.

    The quests are stored in the `quests` table/file as a dict:
      {"last_reset": "YYYY-MM-DD", "quests": [ ... ], "refresh_attempts": 0}

    The system now supports:
      - get_quests(): returns the active quest list
      - update_progress(name, amount): counts quest progress
      - claim_reward(name): grants 10 coins once per completed quest
      - record_app_open(): gives one refresh attempt per app launch
      - refresh_daily_quests(): swaps the daily quest set when an attempt exists
    """

    def __init__(self):
        self.db = Database()
        self.filename = "quests"
        self.reward_callback = None

    def _load_store(self):
        raw = self.db.load(self.filename)
        if not isinstance(raw, dict):
            raw = {"last_reset": "", "quests": [], "refresh_attempts": 0, "app_opens": 0, "last_open_date": ""}
            self.db.save(self.filename, raw)
        raw.setdefault("last_reset", "")
        raw.setdefault("quests", [])
        raw.setdefault("refresh_attempts", 0)
        raw.setdefault("app_opens", 0)
        raw.setdefault("last_open_date", "")
        return raw

    def _save_store(self, store):
        self.db.save(self.filename, store)

    # -------------------
    # GET / GENERATE
    # -------------------
    def get_quests(self):
        self.reset_daily_quests()
        store = self._load_store()
        return store["quests"]

    def generate_daily_quests(self):
        """Generate two random quests and save them with today's date."""
        today = str(date.today())
        possible_quests = [
            {
                "name": "Complete 1 task",
                "goal": 1,
                "progress": 0,
                "reward": 20,
                "completed": False,
                "claimed": False,
            },
            {
                "name": "Feed your pet",
                "goal": 1,
                "progress": 0,
                "reward": 10,
                "completed": False,
                "claimed": False,
            },
            {
                "name": "Play with your pet",
                "goal": 1,
                "progress": 0,
                "reward": 15,
                "completed": False,
                "claimed": False,
            },
            {
                "name": "Buy 1 item from the shop",
                "goal": 1,
                "progress": 0,
                "reward": 25,
                "completed": False,
                "claimed": False,
            },
            {
                "name": "Open the app 3 times",
                "goal": 3,
                "progress": 0,
                "reward": 30,
                "completed": False,
                "claimed": False,
            },
            {
                "name": "Reach 80 happiness",
                "goal": 80,
                "progress": 0,
                "reward": 35,
                "completed": False,
                "claimed": False,
            },
            {
                "name": "Reach 80 hunger",
                "goal": 80,
                "progress": 0,
                "reward": 35,
                "completed": False,
                "claimed": False,
            },
            {
                "name": "Collect 5 coins",
                "goal": 5,
                "progress": 0,
                "reward": 18,
                "completed": False,
                "claimed": False,
            },
        ]

        # choose two different quests
        quests = random.sample(possible_quests, 2)
        for quest in quests:
            quest["reward"] = 10

        store = self._load_store()
        store["last_reset"] = today
        store["quests"] = quests
        self._save_store(store)
        return quests

    # -------------------
    # SAVE / UPDATE
    # -------------------
    def save_quests(self, quests):
        store = self._load_store()
        store["quests"] = quests
        self._save_store(store)

    def _grant_reward(self, reward_amount):
        stats = self.db.load("stats") or {}
        current_coins = stats.get("coins", 0)
        next_coins = current_coins + reward_amount
        self.db.update_stats("coins", next_coins)
        if self.reward_callback is not None:
            self.reward_callback(reward_amount)
        return next_coins

    def record_action(self, action_name):
        action_name = str(action_name or "").strip().lower()
        if not action_name:
            return False

        action_map = {
            "feed": ["Feed your pet"],
            "click": ["Play with your pet"],
            "play": ["Play with your pet"],
            "pet": ["Play with your pet"],
            "buy": ["Buy 1 item from the shop"],
            "buy_food": ["Buy 1 item from the shop"],
            "purchase": ["Buy 1 item from the shop"],
            "shop": ["Buy 1 item from the shop"],
            "app_open": ["Open the app 3 times"],
            "open": ["Open the app 3 times"],
        }

        quest_names = action_map.get(action_name, [])
        if not quest_names:
            quest_names = [action_name]

        changed = False
        for quest_name in quest_names:
            if self.update_progress(quest_name):
                changed = True
        return changed

    def update_progress(self, quest_name, amount=1):
        store = self._load_store()
        changed = False
        for q in store["quests"]:
            if q.get("name") != quest_name or q.get("completed", False):
                continue

            q["progress"] = q.get("progress", 0) + amount
            if q["progress"] >= q.get("goal", 1):
                q["progress"] = q.get("goal", 1)
                q["completed"] = True
                if not q.get("claimed", False):
                    q["claimed"] = True
                    reward_amount = q.get("reward", 10)
                    self._grant_reward(reward_amount)
            changed = True
        if changed:
            self._save_store(store)
        return changed

    def get_progress(self, quest_name):
        for q in self.get_quests():
            if q.get("name") == quest_name:
                return q.get("progress", 0)
        return 0

    def count_completed_quests(self):
        return sum(1 for q in self.get_quests() if q.get("completed", False))

    def claim_reward(self, quest_name):
        """Claim the reward for a completed quest. Returns 10 coins once per completed quest."""
        store = self._load_store()
        for q in store["quests"]:
            if q.get("name") == quest_name:
                if not q.get("completed", False):
                    return 0
                if q.get("claimed", False):
                    return 0
                q["claimed"] = True
                reward = 10
                stats = self.db.load("stats") or {}
                coins = stats.get("coins", 0) + reward
                self.db.update_stats("coins", coins)
                self._save_store(store)
                return reward
        return 0

    # -------------------
    # DAILY RESET
    # -------------------
    def record_app_open(self):
        """Give the player one refresh attempt per app-open day."""
        store = self._load_store()
        today = str(date.today())
        if store.get("last_open_date") != today:
            store["last_open_date"] = today
            store["refresh_attempts"] = 1
            store["app_opens"] = 1
        else:
            store["app_opens"] = store.get("app_opens", 0) + 1
        self._save_store(store)
        self.record_action("app_open")
        return store["refresh_attempts"]

    def refresh_daily_quests(self):
        """Use one refresh attempt to replace the current daily quest set."""
        store = self._load_store()
        if store.get("refresh_attempts", 0) <= 0:
            return False

        store["refresh_attempts"] = max(0, store.get("refresh_attempts", 0) - 1)
        self.generate_daily_quests()
        return True

    def reset_daily_quests(self):
        store = self._load_store()
        today = str(date.today())
        if store.get("last_reset") != today:
            if store.get("quests"):
                store["last_reset"] = today
                self._save_store(store)
            else:
                self.generate_daily_quests()