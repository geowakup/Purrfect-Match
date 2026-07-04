from system.quest_system import QuestSystem


class QuestManager(QuestSystem):
    """Backward-compatible wrapper around the shared daily quest system."""

    def __init__(self):
        super().__init__()

    def load_quests(self):
        return self.get_quests()

    def create_default_file(self):
        self.generate_daily_quests()

    def save_quests(self):
        self._save_store(self._load_store())

    def generate_daily_quests(self):
        return super().generate_daily_quests()

    def update_progress(self, quest_title, amount=1):
        return super().update_progress(quest_title, amount)

    def get_quests(self):
        return super().get_quests()