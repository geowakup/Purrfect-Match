from system.database import Database
from system.task_manager import TaskSystem


# INITIALISE DATABASE

db = Database()


# CONNECT SYSTEMS

task_system = TaskSystem()
# HELPER FUNCTION

def display_tasks(tasks):
    print("\n=== TASK LIST ===")
    for i, task in enumerate(tasks):
        status = "✔ Completed" if task["completed"] else "✘ Pending"
        deadline = task.get("deadline", "No deadline")
        print(f"{i}. {task['title']} | {deadline} | {status}")

# DEMO / TEST DATA
print("\n=== ADDING TASKS ===")
task_system.add_task("Complete 1 task (Quest requirement)")
task_system.add_task("Open app 3 times (Quest requirement)")
task_system.add_task("Finish assignment submission")

# Mark one task as complete (testing reward trigger later)
task_system.complete_task(0)

# DISPLAY TASKS
tasks = task_system.get_tasks()
display_tasks(tasks)

# PLACEHOLDER FOR FUTURE SYSTEMS
print("\n=== QUEST SYSTEM CHECK ===")
completed_count = sum(1 for t in tasks if t["completed"])
if completed_count >= 1:
    print("Quest progress achieved! 🎉 Reward unlocked (placeholder).")

print("\n=== PET SYSTEM CHECK ===")
if completed_count > 0:
    print("🐾 Pet is happy because you completed tasks!")
else:
    print("🐾 Pet is waiting for you to complete tasks...")

print("\nSystem running successfully ")
