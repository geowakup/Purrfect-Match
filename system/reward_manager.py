from system.database import Database


class RewardSystem:

    def __init__(self):
        self.db = Database()

        stats = self.db.load("stats")

        if stats is None:
            stats = {
                "app_opens": 0,
                "tasks_completed": 0,
                "coins": 0
            }

        if "coins" not in stats:
            stats["coins"] = 0

        self.stats = stats

    def save(self):
        self.db.save("stats", self.stats)

    def add_reward(self, amount, reason=""):
        self.stats["coins"] += amount
        self.save()

    def spend_reward(self, amount, reason=""):

        if self.stats["coins"] >= amount:

            self.stats["coins"] -= amount
            self.save()
            return True

        return False

    def get_balance(self):
        return self.stats["coins"]                                 