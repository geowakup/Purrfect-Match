import json
import random
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEST_FILE = os.path.join(BASE_DIR, "data", "quests.json")


class QuestManager:
    def __init__(self):
        self.quests = []
        self.last_reset = ""
        self.load_quests()

    def load_quests(self):

        if not os.path.exists(QUEST_FILE):
            self.create_default_file()

        try:
            with open(QUEST_FILE, "r") as file:
                data = json.load(file)

                self.quests = data.get("quests", [])
                self.last_reset = data.get("last_reset", "")

        except Exception:
            self.create_default_file()

    def create_default_file(self):

        default_data = {
            "last_reset": "",
            "quests": []
        }

        with open(QUEST_FILE, "w") as file:
            json.dump(default_data, file, indent=4)

        self.quests = []
        self.last_reset = ""

    def save_quests(self):

        data = {
            "last_reset": self.last_reset,
            "quests": self.quests
        }

        with open(QUEST_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def generate_daily_quests(self):

        today = str(datetime.now().date())

        if self.last_reset == today:
            return

        possible_quests = [
            {
                "title": "Complete 1 task",
                "goal": 1,
                "progress": 0,
                "reward": 20,
                "completed": False,
                "claimed": False
            },
            {
                "title": "Feed your pet",
                "goal": 1,
                "progress": 0,
                "reward": 10,
                "completed": False,
                "claimed": False
            },
            {
                "title": "Open the app 3 times",
                "goal": 3,
                "progress": 0,
                "reward": 30,
                "completed": False,
                "claimed": False
            }
        ]

        self.quests = random.sample(possible_quests, 2)

        self.last_reset = today

        self.save_quests()

    def update_progress(self, quest_title, amount=1):

        for quest in self.quests:

            if quest["title"] == quest_title:

                if not quest["completed"]:

                    quest["progress"] += amount

                    if quest["progress"] >= quest["goal"]:

                        quest["progress"] = quest["goal"]
                        quest["completed"] = True

        self.save_quests()

    def get_quests(self):
        return self.quests