from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame
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

        self.setWindowTitle("Daily Quest")
        self.resize(400, 600)

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
                padding:8px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#FF4F87;
            }
        """)

        self.layout = QVBoxLayout()

        title = QLabel("🐾 Purrfect Match 🐾")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#FF4F87;
        """)

        self.layout.addWidget(title)

        self.pet_label = QLabel("🐱")
        self.pet_label.setAlignment(Qt.AlignCenter)
        self.pet_label.setStyleSheet("font-size:70px;")

        self.layout.addWidget(self.pet_label)

        self.stats = QLabel()
        self.stats.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.stats)

        self.coins = QLabel()
        self.coins.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.coins)

        quest_title = QLabel("Daily Quests")
        quest_title.setAlignment(Qt.AlignCenter)
        quest_title.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
        """)

        self.layout.addWidget(quest_title)

        self.quest_frame = QFrame()
        self.quest_layout = QVBoxLayout()

        self.quest_frame.setLayout(self.quest_layout)

        self.layout.addWidget(self.quest_frame)

        self.feed_button = QPushButton("🍖 Feed Pet")
        self.feed_button.clicked.connect(self.feed_pet)

        self.layout.addWidget(self.feed_button)

        self.status = QLabel("Pet is waiting for food!")
        self.status.setAlignment(Qt.AlignCenter)

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

            label = QLabel(
                f"{quest['progress']}/{quest['goal']} - {quest['name']}"
            )

            label.setStyleSheet("""
                background:white;
                padding:8px;
                border-radius:8px;
            """)

            self.quest_layout.addWidget(label)


    def feed_pet(self):

        if self.rewards.get_balance() >= 10:

            self.rewards.spend_reward(10, "Feed Pet")

            self.quests.update_progress("Complete 1 task")

            self.load_pet()
            self.load_quests()

            self.status.setText("🐱 Yum! Your pet is happy!")

        else:

            self.status.setText("❌ Not enough coins!")     

if __name__ == "__main__":
    import sys
    from  PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    window = DailyQuestApp()
    window.show()

    sys.exit(app.exec())    