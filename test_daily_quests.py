from system.database import Database
from system.quest_system import QuestSystem


def run_quest_demo():
    quest_system = QuestSystem()
    quest_system.generate_daily_quests()
    quests = quest_system.get_quests()

    print("\n=== DAILY QUESTS ===")
    for quest in quests:
        print(f"Quest: {quest['name']}")
        print(f"Goal: {quest['goal']}")
        print(f"Reward: {quest['reward']}")
        print(f"Progress: {quest['progress']}")
        print(f"Completed: {quest['completed']}")
        print("----------------------")

    return quests


def test_record_action_completes_feed_and_click_quests(tmp_path):
    quest_system = QuestSystem()
    quest_system.db = Database(str(tmp_path))
    quest_system.filename = "quests"

    rewards = []
    quest_system.reward_callback = lambda amount: rewards.append(amount)

    quest_system.generate_daily_quests()

    quest_system.record_action("feed")
    quest_system.record_action("click")

    quests = quest_system.get_quests()
    feed_quest = next(q for q in quests if q["name"] == "Feed your pet")
    play_quest = next(q for q in quests if q["name"] == "Play with your pet")

    assert feed_quest["progress"] == 1
    assert feed_quest["completed"] is True
    assert play_quest["progress"] == 1
    assert play_quest["completed"] is True
    assert rewards == [10, 10]


if __name__ == "__main__":
    run_quest_demo()
