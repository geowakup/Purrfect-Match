from system. database import Database

class QuestSystem:
    def __init__(self):
        self.db = Database()
        self.filename = "quests.json"

    # -------------------
    # GET QUESTS
    # -------------------
    def get_quests(self):
        quests = self.db.load(self.filename)

        # if no quests, create default
        if quests is None:
            quests = [
                {
                    "name": "Complete 1 task",
                    "progress": 0,
                    "goal": 1,
                    "reward" : 20,
                    "completed": False
                },
                {
                    "name": "Open app 3 times",
                    "progress": 0,
                    "goal": 3,
                    "reward" : 30,
                    "completed": False
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
    # UPDATE PROGRESS
    # -------------------
    def update_progress(self, quest_name, amount=1):
        quests = self.get_quests()

        for quest in quests:
            if quest["name"] == quest_name and not quest["completed"]:
                quest["progress"] += amount

                if quest["progress"] >= quest["goal"]:
                    quest["completed"] = True

        self.save_quests(quests)

    def reset_daily_quests(self):
      quests = self.get_quests()

      for quest in quests:
        quest["progress"] = 0
        quest["completed"] = False

      self.db.save(self.filename, quests)

      print("Daily quests reset successfully.")  