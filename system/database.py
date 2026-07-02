import json
import os
from datetime import datetime


class Database:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder

        os.makedirs(self.data_folder, exist_ok=True)

        # define your "tables"
        self.files = {
    "pet": "pet.json",
    "tasks": "tasks.json",
    "stats": "stats.json",
    "quests": "quests.json"
}
        
        self._initialize_files()
    # -------------------------
    # INITIALIZATION
    # -------------------------
    def _initialize_files(self):
        """Create JSON files if they don't exist"""
        defaults = {
    "pet": {
        "food": 50,
        "happiness": 50,
        "level": 1,
        "last_updated": str(datetime.now())
    },
    "tasks": [],
    "quests": [],
    "stats": {
        "app_opens": 0,
        "tasks_completed": 0,
        "coins": 0
    }
}

        for key, file in self.files.items():
            path = os.path.join(self.data_folder, file)

            if not os.path.exists(path):
                self.save(key, defaults[key])

    # -------------------------
    # LOAD DATA
    # -------------------------
    def load(self, name):
        """Load data from JSON file"""
        path = os.path.join(self.data_folder, self.files[name])

        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return None

    # -------------------------
    # SAVE DATA
    # -------------------------
    def save(self, name, data):
        """Save data to JSON file safely"""
        path = os.path.join(self.data_folder, self.files[name])

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    # -------------------------
    # UPDATE SINGLE VALUE
    # -------------------------
    def update_pet(self, key, value):
        pet = self.load("pet")
        pet[key] = value
        self.save("pet", pet)

    def update_stats(self, key, value):
        stats = self.load("stats")
        stats[key] = value
        self.save("stats", stats)

    # -------------------------
    # ADD TASK
    # -------------------------
    def add_task(self, task):
        tasks = self.load("tasks")
        tasks.append(task)
        self.save("tasks", tasks)

    # -------------------------
    # UPDATE TASKS
    # -------------------------
    def update_tasks(self, tasks):
        self.save("tasks", tasks)

    # -------------------------
    # RESET DATABASE (debug tool)
    # -------------------------
    def reset_all(self):
        for key in self.files:
            self.save(key, [])