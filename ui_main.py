from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame,
    QMessageBox,
    QProgressBar
)

from PySide6.QtCore import Qt

from system.quest_system import QuestSystem
from system.reward_manager import RewardSystem
from system.pet_system import PetSystem


class DailyQuestApp(QWidget):

    def __init__(self):
        super().__init__()

        self.quests = QuestSystem()
        self.rewards = RewardSystem()
        self.pet = PetSystem()

        self.setWindowTitle("🐾 Daily Quest")
        self.resize(500,700)

        self.setStyleSheet("""
            QWidget{
                background:#FFE4EC;
            }

            QLabel{
                font-size:14px;
            }

            QPushButton{
                background:#FF69B4;
                color:white;
                border-radius:10px;
                padding:10px;
                font-weight:bold;
                font-size:14px;
            }

            QPushButton:hover{
                background:#FF4F87;
            }
        """)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)

        title = QLabel("🐾 Purrfect Match 🐾")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#FF4F87;
        """)

        self.layout.addWidget(title)

        self.pet_label = QLabel("🐱")
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setStyleSheet("""
            font-size:72px;
        """)

        self.layout.addWidget(self.pet_label)

        self.stats = QLabel()
        self.stats.setAlignment(Qt.AlignCenter)
        self.stats.setStyleSheet("""
            font-size:15px;
            font-weight:bold;
        """)

        self.layout.addWidget(self.stats)

        self.coins = QLabel()
        self.coins.setAlignment(Qt.AlignCenter)
        self.coins.setStyleSheet("""
            font-size:16px;
            font-weight:bold;
            color:#D68910;
        """)

        self.layout.addWidget(self.coins)

        quest_title = QLabel("🎯 Daily Quests")
        quest_title.setAlignment(Qt.AlignCenter)
        quest_title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
            color:#FF4F87;
        """)

        self.layout.addWidget(quest_title)

        self.quest_frame = QFrame()
        self.quest_layout = QVBoxLayout()
        self.quest_layout.setSpacing(10)

        self.quest_frame.setLayout(self.quest_layout)

        self.layout.addWidget(self.quest_frame)

        self.feed_button = QPushButton("🍖 Feed Pet")
        self.feed_button.clicked.connect(self.feed_pet)

        self.layout.addWidget(self.feed_button)

        self.status = QLabel("🐱 Pet is waiting for food!")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("""
            font-weight:bold;
            color:#FF4F87;
        """)

        self.layout.addWidget(self.status)

        self.setLayout(self.layout)

        self.load_pet()
        self.load_quests()

    def load_pet(self):

        pet = self.pet.get_pet()

        self.stats.setText(
            f"🍖 Hunger: {pet['food']}\n"
            f"😊 Happiness: {pet['happiness']}"
        )

        self.coins.setText(
            f"🪙 Coins: {self.rewards.get_balance()}"
        )


    def load_quests(self):

        while self.quest_layout.count():
            child = self.quest_layout.takeAt(0)

            if child.widget():
                child.widget().deleteLater()

        quests = self.quests.get_quests()

        for quest in quests:

            if quest["completed"] and not quest.get("reward_claimed", False):

                self.rewards.add_reward(
                    quest["reward"],
                    quest["name"]
                )

                QMessageBox.information(
                    self,
                    "🎉 Quest Completed!",
                    f"You earned {quest['reward']} Coins!\n\nKeep it up!"
                )

                quest["reward_claimed"] = True
                self.quests.save_quests(quests)

            card = QFrame()

            if quest["completed"]:
                card.setStyleSheet("""
                    background:#D5F5E3;
                    border:2px solid #58D68D;
                    border-radius:12px;
                    padding:15px;
                """)
            else:
                card.setStyleSheet("""
                    background:white;
                    border:2px solid #F5B7B1;
                    border-radius:12px;
                    padding:8px;
                """)

            card_layout = QVBoxLayout()
            card_layout.setSpacing(5)
            card_layout.setContentsMargins(10, 10, 10, 10)

            if quest["completed"]:
                status = QLabel("✅ COMPLETED")
                status.setStyleSheet("""
                    color:green;
                    font-weight:bold;
                    font-size:15px;
                """)
                card_layout.addWidget(status)

            title = QLabel(f"🐾 {quest['name']}")
            title.setStyleSheet("""
                font-size:16px;
                font-weight:bold;
            """)

            card_layout.addWidget(title)

            progress = QLabel(
                f"📊 Progress : {quest['progress']} / {quest['goal']}"
            )

            card_layout.addWidget(progress)

            reward = QLabel(
                f"🪙 Reward : {quest['reward']} Coins"
            )

            reward.setStyleSheet("""
                color:#D68910;
                font-weight:bold;
            """)

            card_layout.addWidget(reward)

            progress_bar = QProgressBar()
            progress_bar.setMaximum(quest["goal"])
            progress_bar.setValue(quest["progress"])
            progress_bar.setTextVisible(False)

            progress_bar.setStyleSheet("""
                QProgressBar{
                    border:2px solid #FFB69B4;
                    border-radius:8px;
                    background:#FFE4EC;                   
                    text-align:center;
                    height:18px;
                }

                QProgressBar::chunk{
                    background:#FF69B4;
                    border-radius:8px;
                }
            """)

            card_layout.addWidget(progress_bar)

            card.setLayout(card_layout)

            self.quest_layout.addWidget(card)

        self.load_pet()


    def feed_pet(self):

        if self.rewards.spend_reward(10, "Feed Pet"):

            self.pet.give_reward(food=10, happiness=5)

            self.load_pet()

            self.status.setText("😸 Yum! Your pet loved the food!")

        else:

            self.status.setText("❌ Not enough coins!")


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    window = DailyQuestApp()
    window.show()

    sys.exit(app.exec())   