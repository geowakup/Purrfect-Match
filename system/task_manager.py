from system.database import Database

class TaskSystem:
    def __init__(self):
        self.db = Database()
        self.filename = "tasks"

    # -------------------
    # GET ALL TASKS
    # -------------------
    def get_tasks(self):
        tasks = self.db.load(self.filename)
        if tasks is None:
            return []
        return tasks

    # -------------------
    # ADD TASK
    # -------------------
    def add_task(self, task_name):
        tasks = self.get_tasks()

        new_task = {
            "task": task_name,
            "done": False
        }

        tasks.append(new_task)
        self.db.save(self.filename, tasks)

    # -------------------
    # MARK TASK AS DONE
    # -------------------
    def complete_task(self, index):
        tasks = self.get_tasks()

        if 0 <= index < len(tasks):
            tasks[index]["done"] = True

        self.db.save(self.filename, tasks)

    # -------------------
    # DELETE TASK
    # -------------------
    def delete_task(self, index):
        tasks = self.get_tasks()

        if 0 <= index < len(tasks):
            tasks.pop(index)

        self.db.save(self.filename, tasks)