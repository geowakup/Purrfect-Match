from system.pet_manager import Pet
from system.reward_manager import RewardSystem
from system.task_manager import TaskSystem
from system.quest_system import QuestSystem
from system.database import Database
import time

def run_demo():
    db = Database("data.json")
    pet = Pet("Buddy")
    rewards = RewardSystem()
    tasks = TaskSystem()
    quests = QuestSystem()

    # Update pet state
    pet.update()
    print("Pet state:", pet.get_state())
    
    
    # Add and complete a task
    tasks.add_task("Finish coding project")
    tasks.complete_task(0)
    rewards.add_reward(20, "Completed a task")
    if rewards.get_balance() >= 10:
        pet.feed(20)
        rewards.spend_reward(10, "Fed the pet")
        print("Pet fed successfully!")
    else:
        print("Not enough coins to feed pet.")
        print("After feeding:", pet.get_state())

    print("Tasks:", tasks.get_tasks())

    # Quest progress
    quests.update_progress("Complete 1 task")
    quests.update_progress("Open app 3 times")
    quests.update_progress("Open app 3 times")
    quests.update_progress("Open app 3 times")
    quests.update_progress("Open app 3 times")
    print("Quests:", quests.get_quests())
    quests.reset_daily_quests()

    # Save everything
    db.save("pets", [pet.get_state()])
    db.save("tasks", tasks.get_tasks())
    db.save("quests.json", quests.get_quests())
    db.save("stats", {"coins": rewards.get_balance()})
    print("Database saved successfully.")


if __name__ == "__main__":
    run_demo()

