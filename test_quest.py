from system.quests_manager import QuestManager

quest_manager = QuestManager()

quest_manager.generate_daily_quests()

quests = quest_manager.get_quests()

print("\n=== DAILY QUESTS ===")

for quest in quests:

    print(f"Quest: {quest['title']}")
    print(f"Goal: {quest['goal']}")
    print(f"Reward: {quest['reward']}")
    print(f"Progress: {quest['progress']}")
    print(f"Completed: {quest['completed']}")
    print("----------------------")