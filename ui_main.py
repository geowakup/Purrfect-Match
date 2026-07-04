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
﻿from system.reward_manager import RewardSystem
from system.quest_system import QuestSystem
import tkinter as tk


class PurrfectMatchApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Purrfect Match 🐾")
        self.window.geometry("520x700")
        self.window.configure(bg="#FFE4EC")

        self.quest_system = QuestSystem()
        self.rewards = RewardSystem()
        self.hunger = 100
        self.happiness = 100

        self.rewards.add_reward(20, "Starting coins")
        self.quest_system.update_progress("Open app 3 times")

        self.create_ui()
        self.load_quests()
        self.update_header()
        self.decay()

        self.window.mainloop()

    def create_ui(self):
        title = tk.Label(
            self.window,
            text="🐾 Purrfect Match 🐾",
            font=("Comic Sans MS", 24, "bold"),
            bg="#FFE4EC",
            fg="#FF4F87"
        )
        title.pack(pady=15)

        pet_frame = tk.Frame(self.window, bg="#FFF0F5", bd=2, relief="ridge")
        pet_frame.pack(padx=20, pady=10, fill="x")

        self.pet_label = tk.Label(
            pet_frame,
            text="🐱",
            font=("Arial", 70),
            bg="#FFF0F5"
        )
        self.pet_label.pack(pady=10)

        self.stats_label = tk.Label(
            pet_frame,
            text="🍖 Hunger: 100\n😊 Happiness: 100",
            font=("Comic Sans MS", 13),
            bg="#FFF0F5",
            fg="#8B3A62",
            padx=10,
            pady=10,
            justify="left"
        )
        self.stats_label.pack(pady=5)

        self.coins_label = tk.Label(
            pet_frame,
            text="Coins: 0",
            font=("Comic Sans MS", 14, "bold"),
            bg="#FFF0F5",
            fg="#C71585",
            padx=10,
            pady=6
        )
        self.coins_label.pack(pady=5)

        self.status_label = tk.Label(
            self.window,
            text="🐱 Pet is waiting for food!",
            font=("Segoe UI", 12),
            bg="#FFE4EC",
            fg="#8B3A62"
        )
        self.status_label.pack(pady=8)

        quest_frame = tk.Frame(self.window, bg="#FFE4EC")
        quest_frame.pack(padx=20, pady=10, fill="both", expand=True)

        quest_title = tk.Label(
            quest_frame,
            text="Daily Quests",
            font=("Comic Sans MS", 18, "bold"),
            bg="#FFE4EC",
            fg="#DB3E6F"
        )
        quest_title.pack(pady=(0, 10))

        self.quest_list_frame = tk.Frame(quest_frame, bg="#FFF0F5", bd=2, relief="groove")
        self.quest_list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.refresh_quests_button = tk.Button(
            quest_frame,
            text="Refresh Quests",
            command=self.load_quests,
            font=("Comic Sans MS", 12),
            bg="#FFB6C1",
            fg="white",
            relief="raised",
            bd=3,
            padx=10,
            pady=6
        )
        self.refresh_quests_button.pack(pady=10)

        self.feed_button = tk.Button(
            self.window,
            text="🍖 Feed Pet",
            command=self.feed_pet,
            font=("Comic Sans MS", 14, "bold"),
            bg="#FF69B4",
            fg="white",
            padx=20,
            pady=10,
            relief="raised",
            bd=4
        )
        self.feed_button.pack(pady=15)

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
    def update_header(self):
        self.stats_label.config(
            text=f"🍖 Hunger: {self.hunger}\n😊 Happiness: {self.happiness}"
        )
        self.coins_label.config(
            text=f"Coins: {self.rewards.get_balance()}"
        )

    def load_quests(self):
        for widget in self.quest_list_frame.winfo_children():
            widget.destroy()

        quest_data = self.quest_system.get_quests()

        if not quest_data:
            empty_label = tk.Label(
                self.quest_list_frame,
                text="No quests available.",
                font=("Segoe UI", 12),
                bg="#FFF0F5",
                fg="#8B3A62",
                pady=10
            )
            empty_label.pack(pady=10)
            return

        for quest in quest_data:
            completed_text = " ✅" if quest.get("completed", False) else ""
            quest_text = f"{quest['progress']}/{quest['goal']} - {quest.get('name', quest.get('title', 'Unknown'))}{completed_text}"
            quest_label = tk.Label(
                self.quest_list_frame,
                text=quest_text,
                font=("Segoe UI", 12),
                bg="#FFF0F5",
                fg="#8B3A62",
                anchor="w",
                justify="left",
                padx=10,
                pady=8
            )
            quest_label.pack(fill="x", padx=10, pady=4)

        self.update_header()

    def feed_pet(self):
        if self.rewards.get_balance() < 10:
            self.status_label.config(text="🐱 Not enough coins!")
            return

        self.rewards.spend_reward(10, "Fed pet")
        self.quest_system.update_progress("Complete 1 task")

        self.hunger = min(self.hunger + 10, 100)
        self.happiness = min(self.happiness + 5, 100)

        self.update_header()
        self.load_quests()
        self.status_label.config(text="🐱 Yum! Your pet is happy!")

    def decay(self):
        self.hunger = max(self.hunger - 1, 0)
        self.happiness = max(self.happiness - 1, 0)
        self.update_header()
        self.window.after(5000, self.decay)


if __name__ == "__main__":
    PurrfectMatchApp()
