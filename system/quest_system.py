from system.database import Database
from datetime import date


class QuestSystem:

    def __init__(self):
        self.db = Database()
        self.filename = "quests"
        self.last_reset = str(date.today())

    # -------------------
    # GET QUESTS
    # -------------------
    def get_quests(self):

        self.reset_daily_quests()

        quests = self.db.load(self.filename)

        if quests is None:

            quests = [
                {
                    "name": "Complete 1 task",
                    "progress": 0,
                    "goal": 1,
                    "reward": 20,
                    "completed": False,
                    "reward_claimed": False
                },
                {
                    "name": "Open app 3 times",
                    "progress": 0,
                    "goal": 3,
                    "reward": 30,
                    "completed": False,
                    "reward_claimed": False
                }
            ]

            self.db.save(self.filename, quests)

        return quests

    # -------------------
    # SAVE QUESTS
    # -------------------
    def save_quests(self, quests):
        self.db.save(self.filename, quests)

    # -------------------
    # UPDATE QUEST PROGRESS
    # -------------------
    def update_progress(self, quest_name, amount=1):

        quests = self.get_quests()

        for quest in quests:

            if quest["name"] == quest_name and not quest["completed"]:

                quest["progress"] += amount

                if quest["progress"] >= quest["goal"]:

                    quest["completed"] = True

                    print(f"Quest completed: {quest['name']}")

        self.save_quests(quests)

    # -------------------
    # DAILY RESET
    # -------------------
    def reset_daily_quests(self):

        today = str(date.today())

        if self.last_reset != today:

            quests = self.db.load(self.filename)

            if quests is not None:

                for quest in quests:
                    quest["progress"] = 0
                    quest["completed"] = False
                    quest["reward_claimed"] = False

                self.db.save(self.filename, quests)

            self.last_reset = today

            print("Daily quests reset successfully.")